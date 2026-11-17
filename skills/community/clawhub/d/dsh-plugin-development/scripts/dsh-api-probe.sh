#!/usr/bin/env bash
#
# dsh-api-probe.sh —— 用「当前 DSH 源码」核验本 skill 依赖的易变 API 断言。
#
# 目的：把「信任文档」变成「可执行的断言」。
#       本 skill 的 references 全部冻结在某个 commit 上，DSH 是 rc 阶段、高频变动，
#       因此凡是要写进代码的 API，都应先用本脚本对源码核验一遍。
#
# 用法：
#   bash scripts/dsh-api-probe.sh [DSH 仓库路径] [--quiet]
#
#   不传路径时，依次尝试 ./deepseek-harness、../deepseek-harness、$DSH_REPO。
#
# 退出码：
#   0 = 全部 HOLDS（或只有 SKIP）
#   1 = 存在 STALE（有断言在当前源码中不成立 → 相关模板可能已过时，不要直接照抄）
#   2 = 找不到仓库路径 / 不是 DSH 仓库
#   3 = 断言表为空（环境缺 coreutils）→ 未核验任何事实，结果无效
#
# 设计约束（重要）：
#   * 断言只用「符号/字符串存在性」，**绝不依赖行号** —— 行号必然漂移。
#   * 只断言「一旦消失就会让本 skill 的指引失效」的事实。
#     枚举类事实（命令清单、插槽总数、默认值、报错文案细节）故意不断言，
#     因为新增强功能会让它们天天变，探针会变成狼来了。
#
#   * 断言分两类，**语义相反**，别搞混：
#       正向（S/M/L 级，模式 g/f/d）    ：命中 = 成立（HOLDS）。
#       反向（N 级，模式 nf/nd/nt/nl）  ：**未命中 = 成立（HOLDS）**；
#                                       命中 = 该否定论断已被推翻（STALE）。
#     N 级断言的 payload 写的是「如果这条否定论断错了，会出现的证据」。
#     为什么需要反向断言：本 skill 里有不少「仓库没有 CHANGELOG」「提交不用
#     BREAKING CHANGE 页脚」这类**否定性结论**。它们同样会过时（上游哪天补上
#     CHANGELOG，结论就错了），但普通断言机制抓不到。本 skill 曾因一条错误的
#     否定论断（「DSH 不用 ! 标记破坏性提交」，实为 21 条）误导过一次文档，
#     反向断言就是为了让这类错误能被机器发现，而不是等下一次人工复核。
#
set -uo pipefail

REPO=""
QUIET=0
for a in "$@"; do
  case "$a" in
    --quiet) QUIET=1 ;;
    *) REPO="$a" ;;
  esac
done

if [ -z "$REPO" ]; then
  for c in "./deepseek-harness" "../deepseek-harness" "${DSH_REPO:-}"; do
    [ -n "$c" ] && [ -f "$c/packages/AGENTS.md" ] && REPO="$c" && break
  done
fi
if [ -z "$REPO" ] || [ ! -d "$REPO" ]; then
  echo "ERROR: 找不到 DSH 仓库。请把仓库路径作为第一个参数传入。"
  echo "       （判定标准：目录下存在 packages/AGENTS.md）"
  exit 2
fi

# 仓库识别守卫：防止误把任意目录当成 DSH 仓库，跑出一堆假的 STALE。
if [ ! -d "$REPO/packages" ] || { [ ! -d "$REPO/vendor/loader" ] && [ ! -d "$REPO/apps/cli" ]; }; then
  echo "ERROR: $REPO 看起来不是 DSH 仓库。"
  echo "       期望看到 packages/ 目录，以及 vendor/loader/ 或 apps/cli/ 之一。"
  echo "       （防止对着错误目录跑出假的 STALE 结论）"
  exit 2
fi

# ── 0. 报告核验基线：当前仓库的版本与 commit ────────────────────────────────
BASELINE_COMMIT="f3803c9697"
BASELINE_VER="0.2.2-alpha.2"

LIVE_VER="$(node -e "try{console.log(require('$REPO/package.json').version||'unknown')}catch(e){console.log('unknown')}" 2>/dev/null || echo unknown)"
LIVE_COMMIT="$(git -C "$REPO" rev-parse --short=10 HEAD 2>/dev/null || echo unknown)"
LIVE_DATE="$(git -C "$REPO" log -1 --format=%cs 2>/dev/null || echo unknown)"

if [ "$QUIET" -eq 0 ]; then
  echo "════════════════════════════════════════════════════════════════"
  echo " DSH API 探针"
  echo "════════════════════════════════════════════════════════════════"
  echo " 仓库路径   : $REPO"
  echo " 当前版本   : $LIVE_VER   (HEAD $LIVE_COMMIT, $LIVE_DATE)"
  echo " skill 基线 : $BASELINE_VER   ($BASELINE_COMMIT)"
  if [ "$LIVE_COMMIT" = "unknown" ]; then
    echo " ⚠️  无法读取 git HEAD（不是 git 仓库或没有 git）——版本比对已跳过。"
  elif [ "${LIVE_COMMIT:0:10}" = "${BASELINE_COMMIT:0:10}" ]; then
    echo " ✅  与基线同一 commit —— references 可直接使用。"
  else
    echo " ⚠️  commit 与基线不同 —— references 仍需核验，不要无条件照抄。"
    BREAKS="$(git -C "$REPO" log --oneline --grep='!' "${BASELINE_COMMIT}..HEAD" 2>/dev/null | wc -l | tr -d ' ')"
    if [ "$BREAKS" != "0" ] && [ "$BREAKS" != "" ]; then
      echo " 🔴  基线之后检测到 $BREAKS 条破坏性提交（标题含 !）。"
      echo "     先跑: git -C \"$REPO\" log --oneline --grep='!' ${BASELINE_COMMIT}..HEAD"
    else
      echo " ℹ️   基线之后未检测到含 '!' 的破坏性提交标题（不代表一定无破坏性变更）。"
    fi
  fi
  echo
fi

# ── 1. 断言表 ────────────────────────────────────────────────────────────────
# 格式：ID,等级,说明,模式,作用域
#   等级：S = 结构性公理（衰减极慢） / M = 接口名（每次使用前核验）
#         N = 否定性论断（语义反向：未命中 = HOLDS；命中 = STALE）
#   模式：g:<ERE> 用 grep 核验 / f:<相对路径> 文件必须存在 / d:<相对路径> 目录必须存在
#         N 级：nf:<文件名> / nd:<目录名> / nt:<tag 正则> / nl:<提交信息正则> / na:<内容正则>
#         `na:` 是 2026-09-16 新增的**内容**否定模式，用于「旧名已被改名取代且无别名」这类结论。
# 断言表内联为字符串字面量（**不要改回 `cat <<'EOF'` 形式**）。
# 原因：本机 Git Bash 环境缺 `cat` 等 coreutils，`$(cat <<EOF ... )` 会静默展开为空
# → 断言表为空 → total=0 却被判为「全部成立」并 exit 0。
# 这类「静默通过」比报错危险得多，故：① 改用内联字符串；② 见下方空表哨兵。
CHECKS='S01,S,插件导出形态硬规则（函数式插件不得有 default export）,g:service packages default-export their service class,packages/AGENTS.md
S02,S,复盘 0001（default export 丢弃命名空间）仍在档,f:docs/postmortem/0001-acp-default-export-drops-inject.md,-
S03,S,服务类继承形态仍存在,g:extends Service,packages
S04,S,补丁行序无语义（激活由服务可用性驱动）,g:Row order carries no load semantics,packages
S05,S,纯配置组合包范式（src/index.ts 只导出空对象）,g:export \{\},packages/bundle/base/src/index.ts
S06,S,base 补丁含 !!js 内联表达式,g:!!js,packages/bundle/base
M01,M,defineTool 从 dsh-tools 导出,g:export (function|const) defineTool,packages
M02,M,DSH 参数 DSL：属性级 required,g:ParameterPropertySpec = ValueSchemaSpec & \{ required\?: true \},packages
M03,M,属性级 required 的校验报错文案,g:required must be true when present,packages
M04,M,对象级 required 必须是数组（裸 register 路径）,g:required must be an array of strings,packages
M05,M,DefineToolOptions 接口,g:interface DefineToolOptions,packages
M06,M,工具注册 API,g:tools\.register\(,packages
M07,M,命令注册 API,g:commands\.register\(,packages
M08,M,UI 插槽 API,g:slots\.(inject|register)\(,packages
M09,M,服务插件构造函数首参约定,g:super\(ctx[^)]*'"'"',packages
M10,M,dsh.bundle 声明缺失时的警告,g:declares no dsh\.bundle,packages
M11,M,loader 非事务化（补丁行应用失败只记日志、不回滚）,g:Wait until this tree has no pending import,vendor/loader
M12,M,子进程凭据清洗正则常量,g:SENSITIVE_ENV_PATTERN,packages
M13,M,补丁内相对路径锚定函数,g:anchorInsertedPluginNames,packages
M14,M,保留工具名 run_code,g:run_code,packages
M15,M,配置树导出开关,g:\-\-dump-config,packages
M16,M,插件安装 CLI,g:dsh plugin,apps
M17,M,事件 agent/pre-step,g:agent/pre-step,packages
M18,M,事件 agent/request,g:agent/request,packages
M19,M,事件 agent/turn-stopping,g:agent/turn-stopping,packages
M20,M,事件 llm/stream,g:llm/stream,packages
M21,M,事件 system-prompt/assemble,g:system-prompt/assemble,packages
M22,M,事件 approval/request,g:approval/request,packages
M23,M,插槽 settings.section,g:settings\.section,packages
M24,M,插槽 conversation.view,g:conversation\.view,packages
M25,M,插槽 tool.call.toolview,g:tool\.call\.toolview,packages
M26,M,DSH_HOME 路径辅助函数,g:dshHomePath,packages
M27,M,可选服务的拓扑无关取法,g:ctx\.get\(,packages
M28,M,副作用回收 API,g:ctx\.effect\(,packages
M29,M,waterfall 放行约定,g:await next\(\),packages
M30,M,timeoutMs 正值校验文案,g:timeoutMs must be a positive finite number,packages
M31,M,dsh.bundle 清单字段,g:dsh\.bundle,packages
M32,M,DSH_HOME 环境变量,g:DSH_HOME,packages
M33,M,服务 ctx.ptcRuntime（原 codeRuntime 改名，不提供别名）,g:ptcRuntime,packages/ptc-runtime
M34,M,服务 ctx.mcpResources,g:mcpResources,packages/mcp/mcp-resources
M35,M,PreToolDecision 新增 cancel 决策,g:kind: '"'"'cancel'"'"',packages/core/tools
M36,M,base 补丁新增 image-offload 插件行,g:image-offload,packages/bundle/base/cordis.patch.yml
M37,M,base 补丁的 workflow 行改用 ptc 家族,g:workflow-ptc,packages/bundle/base/cordis.patch.yml
L01,L,官方插件工程约定入口,f:packages/AGENTS.md,-
L02,L,loader 配置校验实现,f:vendor/loader/src/config/group.ts,-
L03,L,CLI 插件安装实现,f:apps/cli/src/plugin.ts,-
L04,L,官方纯配置组合包补丁,f:packages/bundle/base/cordis.patch.yml,-
L05,L,顶层目录布局（packages/vendor/apps/docs）,d:vendor,-
N01,N,仓库没有 CHANGELOG 文件（变更史只在 git 与 .agents/notes）,nf:CHANGELOG*,-
N02,N,提交不使用 BREAKING CHANGE 页脚（只用 type(scope)!: 标题标记）,nl:BREAKING CHANGE,-
N03,N,不存在 packages/ui/（TUI 前端已归档）,nd:ui,packages
N04,N,版本号不连续：不存在 0.1.4,nt:0\.1\.4,-
N05,N,不采用 changesets 发布流程（无 .changeset/）,nf:.changeset,-
N06,N,旧服务名 codeRuntime 已无兼容别名,na:ctx\.codeRuntime,packages
N07,N,事件 agent/session-start 已被 serial 的 agent/created 取代,na:agent/session-start,packages
N08,N,E2B 执行后端已整体移除,na:deepseek-ai/dsh-e2b,packages'

# ── 1b. 空表哨兵 ────────────────────────────────────────────────────────────
# 断言表为空 = 探针什么都没核验。绝不能报「全部成立」。
if [ -z "$CHECKS" ]; then
  echo "🔴 断言表为空 —— 探针未核验任何事实，结果无效。"
  echo "   常见原因：shell 缺少 coreutils（cat/find/grep）导致文本块展开失败。"
  echo "   请改用含完整 coreutils 的 bash（如 Git for Windows 的 bash.exe）重跑。"
  exit 3
fi

# ── 2. 逐条核验 ──────────────────────────────────────────────────────────────
# 注意：解析必须校验字段数。逗号是分隔符，若某条断言的模式里混入逗号，
# 字段会被多切一刀、作用域被静默截错 —— 那会让探针报出假结果。
HOLDS=0; STALE=0; SKIP=0; TOTAL=0; PARSE_ERR=0; NEG=0
STALE_ROWS=""
SKIP_ROWS=""

while IFS= read -r line; do
  [ -z "$line" ] && continue
  IFS=',' read -r -a F <<< "$line"
  if [ "${#F[@]}" -ne 5 ]; then
    PARSE_ERR=$((PARSE_ERR + 1))
    STALE_ROWS="$STALE_ROWS
  PARSE  断言表解析失败（字段数 ${#F[@]} != 5，模式里可能混入了逗号）
        原文: $line"
    printf '  \033[31mPARSE\033[0m 断言表字段数异常（%s != 5）: %s\n' "${#F[@]}" "$line"
    continue
  fi
  id="${F[0]}"; tier="${F[1]}"; desc="${F[2]}"; mode="${F[3]}"; scope="${F[4]}"
  [ "$scope" = "-" ] && scope=""
  TOTAL=$((TOTAL + 1))
  [ "$tier" = "N" ] && NEG=$((NEG + 1))
  kind="${mode%%:*}"
  payload="${mode#*:}"
  target="$REPO"
  [ -n "$scope" ] && target="$REPO/$scope"

  case "$kind" in
    g)
      if [ ! -e "$target" ]; then
        SKIP=$((SKIP + 1)); SKIP_ROWS="$SKIP_ROWS
  $id  [$tier] 作用域缺失: $scope"
      elif grep -rqE -- "$payload" "$target" 2>/dev/null; then
        HOLDS=$((HOLDS + 1))
        [ "$QUIET" -eq 0 ] && printf '  \033[32mHOLDS\033[0m  %-4s [%s] %s\n' "$id" "$tier" "$desc"
      else
        STALE=$((STALE + 1)); STALE_ROWS="$STALE_ROWS
  $id  [$tier] $desc
        期望模式: $payload
        作用域  : $scope"
        [ "$QUIET" -eq 0 ] && printf '  \033[31mSTALE\033[0m  %-4s [%s] %s\n' "$id" "$tier" "$desc"
      fi ;;
    f)
      if [ -e "$target/$payload" ]; then
        HOLDS=$((HOLDS + 1))
        [ "$QUIET" -eq 0 ] && printf '  \033[32mHOLDS\033[0m  %-4s [%s] %s\n' "$id" "$tier" "$desc"
      else
        STALE=$((STALE + 1)); STALE_ROWS="$STALE_ROWS
  $id  [$tier] $desc
        缺失文件: $scope$payload"
        [ "$QUIET" -eq 0 ] && printf '  \033[31mSTALE\033[0m  %-4s [%s] %s\n' "$id" "$tier" "$desc"
      fi ;;
    d)
      if [ -d "$target/$payload" ]; then
        HOLDS=$((HOLDS + 1))
        [ "$QUIET" -eq 0 ] && printf '  \033[32mHOLDS\033[0m  %-4s [%s] %s\n' "$id" "$tier" "$desc"
      else
        STALE=$((STALE + 1)); STALE_ROWS="$STALE_ROWS
  $id  [$tier] $desc
        缺失目录: $payload"
        [ "$QUIET" -eq 0 ] && printf '  \033[31mSTALE\033[0m  %-4s [%s] %s\n' "$id" "$tier" "$desc"
      fi ;;
    # ── N 级反向断言：断言「某物不存在」。命中即否定论断被推翻。 ──────────
    nf)
      hit=$(find "$target" -iname "$payload" \
              -not -path '*/node_modules/*' -not -path '*/.git/*' 2>/dev/null | head -3)
      if [ -z "$hit" ]; then
        HOLDS=$((HOLDS + 1))
        [ "$QUIET" -eq 0 ] && printf '  \033[32mHOLDS\033[0m  %-4s [%s] %s\n' "$id" "$tier" "$desc"
      else
        STALE=$((STALE + 1)); STALE_ROWS="$STALE_ROWS
  $id  [$tier] 否定论断已被推翻：$desc
        断言不存在，却找到: $(echo "$hit" | tr '\n' ' ')"
        [ "$QUIET" -eq 0 ] && printf '  \033[31mSTALE\033[0m  %-4s [%s] %s（否定论断失效）\n' "$id" "$tier" "$desc"
      fi ;;
    nd)
      if [ ! -d "$target/$payload" ]; then
        HOLDS=$((HOLDS + 1))
        [ "$QUIET" -eq 0 ] && printf '  \033[32mHOLDS\033[0m  %-4s [%s] %s\n' "$id" "$tier" "$desc"
      else
        STALE=$((STALE + 1)); STALE_ROWS="$STALE_ROWS
  $id  [$tier] 否定论断已被推翻：$desc
        断言不存在的目录已出现: $scope/$payload"
        [ "$QUIET" -eq 0 ] && printf '  \033[31mSTALE\033[0m  %-4s [%s] %s（否定论断失效）\n' "$id" "$tier" "$desc"
      fi ;;
    # na：内容否定（2026-09-16 新增）。前四个模式只能否定「文件/目录/tag/提交信息」，
    # 而「旧服务名无别名」「旧事件名被取代」「某后端整体移除」的过时方向是内容里又冒出旧字符串。
    na)
      if [ ! -e "$target" ]; then
        SKIP=$((SKIP + 1)); SKIP_ROWS="$SKIP_ROWS
  $id  [$tier] 作用域缺失: $scope"
      elif hit=$(grep -rnE -- "$payload" "$target" 2>/dev/null | head -3) && [ -n "$hit" ]; then
        STALE=$((STALE + 1)); STALE_ROWS="$STALE_ROWS
  $id  [$tier] 否定论断已被推翻：$desc
        断言不应再出现，却命中: $(echo "$hit" | tr '\n' ' ')"
        [ "$QUIET" -eq 0 ] && printf '  \033[31mSTALE\033[0m  %-4s [%s] %s（否定论断失效）\n' "$id" "$tier" "$desc"
      else
        HOLDS=$((HOLDS + 1))
        [ "$QUIET" -eq 0 ] && printf '  \033[32mHOLDS\033[0m  %-4s [%s] %s\n' "$id" "$tier" "$desc"
      fi ;;
    nt)
      if ! git -C "$REPO" rev-parse --git-dir >/dev/null 2>&1; then
        SKIP=$((SKIP + 1)); SKIP_ROWS="$SKIP_ROWS
  $id  [$tier] 非 git 仓库，无法核验 tag"
      elif git -C "$REPO" tag 2>/dev/null | grep -qE -- "$payload"; then
        STALE=$((STALE + 1)); STALE_ROWS="$STALE_ROWS
  $id  [$tier] 否定论断已被推翻：$desc
        匹配到的 tag: $(git -C "$REPO" tag 2>/dev/null | grep -E -- "$payload" | head -3 | tr '\n' ' ')"
        [ "$QUIET" -eq 0 ] && printf '  \033[31mSTALE\033[0m  %-4s [%s] %s（否定论断失效）\n' "$id" "$tier" "$desc"
      else
        HOLDS=$((HOLDS + 1))
        [ "$QUIET" -eq 0 ] && printf '  \033[32mHOLDS\033[0m  %-4s [%s] %s\n' "$id" "$tier" "$desc"
      fi ;;
    nl)
      if ! git -C "$REPO" rev-parse --git-dir >/dev/null 2>&1; then
        SKIP=$((SKIP + 1)); SKIP_ROWS="$SKIP_ROWS
  $id  [$tier] 非 git 仓库，无法核验提交历史"
      elif git -C "$REPO" log --all --format='%s%n%b' 2>/dev/null | grep -qE -- "$payload"; then
        STALE=$((STALE + 1)); STALE_ROWS="$STALE_ROWS
  $id  [$tier] 否定论断已被推翻：$desc
        提交信息中匹配到: $payload
        复核: git -C <repo> log --all --grep='$payload'"
        [ "$QUIET" -eq 0 ] && printf '  \033[31mSTALE\033[0m  %-4s [%s] %s（否定论断失效）\n' "$id" "$tier" "$desc"
      else
        HOLDS=$((HOLDS + 1))
        [ "$QUIET" -eq 0 ] && printf '  \033[32mHOLDS\033[0m  %-4s [%s] %s\n' "$id" "$tier" "$desc"
      fi ;;
    *)
      PARSE_ERR=$((PARSE_ERR + 1))
      STALE_ROWS="$STALE_ROWS
  $id  未知的检查类型: $kind" ;;
  esac
done <<< "$CHECKS"

# ── 3. 结论 ──────────────────────────────────────────────────────────────────
echo
echo "────────────────────────────────────────────────────────────────"
echo "SUMMARY total=$TOTAL positive=$((TOTAL - NEG)) negative=$NEG holds=$HOLDS stale=$STALE skipped=$SKIP parse_errors=$PARSE_ERR"

if [ "$PARSE_ERR" -gt 0 ]; then
  echo
  echo "🔴 断言表自身有解析错误 —— 探针结果不可信，先修断言表再判断是否过时。"
  echo "$STALE_ROWS"
  exit 1
fi

if [ "$STALE" -gt 0 ]; then
  echo
  echo "🔴 有断言不成立 —— 相关模板/速查表可能已过时，**不要直接照抄**："
  echo "$STALE_ROWS"
  echo
  echo "处理办法（见 references/00-version-gate.md）："
  echo "  1) 以源码为准，从当前源码重新推导该 API 的正确用法；"
  echo "  2) 把结论写进 ~/.workbuddy/memory/ 并在交付物里注明「已对 <commit> 核验」；"
  echo "  3) 更新 references/api-claims.md 与本脚本的断言表，然后重跑本探针。"
  echo
  echo "  ⚠️ 若 STALE 来自 N 级反向断言 —— 那不是「上游 API 过时」，而是"
  echo "     **本 skill 的一条否定结论已被推翻**（如「存在某文件」推翻了「没有该文件」）。"
  echo "     这类错误方向相反且更隐蔽：必须修正 api-claims.md 的该条，并 grep 全库"
  echo "     找出所有引用了该结论的文档一并改正 —— 不能只改一处。"
  exit 1
fi

if [ "$SKIP" -gt 0 ]; then
  echo "⚠️  有作用域缺失（可能是仓库不完整或布局变了）：$SKIP_ROWS"
fi
echo "✅ 全部断言成立 —— references 中 M 级事实对当前源码有效。"
echo "   注意：本结果只覆盖「探针断言过的事实」，不覆盖 V 级细节（默认值/枚举/文案）。"
exit 0
