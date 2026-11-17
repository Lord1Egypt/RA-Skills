# 工作台标准检验流程（Workbench QA Standard）

> 适用范围：`workbench/` 下的工作台页面（前端 `workbench.html` + 后端 `server.py` + 契约层 `form_schema.py`）。
> 这是 **ct-samplesize 技能的强制质量闸门**：任何对工作台源码的改动，发布前必须跑通本流程。
> 英文 canonical 版：[workbench_qa.md](workbench_qa.md)
> 测试套件实操细节：[../workbench/autotest/README.md](../workbench/autotest/README.md)

---

## 一、定位与强制闸门

工作台是单文件应用（`workbench.html` 约 2700 行，内联 CSS/JS）+ 后端 `server.py`（stdlib `http.server`，REST + 静态资源）+ 契约层 `form_schema.py`。三者任一漂移都会表现为「页面点不动 / 结果不对 / 线上跑的不是这份代码」。因此本流程**同时覆盖静态契约、后端接口、浏览器内行为、真实用户流程、布局可访问性五个面**，不是只测其中一块。

**强制闸门（release gate）—— 满足任一条件即必须全量跑通：**

1. 修改了 `workbench.html` / `server.py` / `form_schema.py` / `tokens.css` / `wb-list.css` / `wb-list.js` 任一文件；
2. 准备执行 `publish-kit/build_publish.py` 或 `install_genie.py`（即发布工作台载荷 / 上线应用）之前；
3. 发布后线上回归（见 §5）。

闸门判据：**5 层全部 green（0 failed / 0 error）**。任一用例失败 = 不允许发布。

---

## 二、五层架构

| 层 | 名称 | 手段 | 不依赖 | 典型抓到的 bug 类型 |
|---|---|---|---|---|
| **L1** | 静态契约 | 纯 Python 解析 HTML（不启浏览器/后端） | 浏览器、后端 | id 冲突、事件处理器指向未定义函数、i18n key 缺失、硬编码中文、`debugger`/`console` 残留、JS 语法不可解析、发布产物漂移 |
| **L2** | 后端 API 契约 | 起 `server.py` 子进程 + requests | 浏览器 | 5xx 崩溃、非法输入未拦截（应 4xx）、凭据文件被 HTTP 下载、会话生命周期、限流失效 |
| **L3** | 前端单元 | Playwright 内直接调用页面 JS | 真实交互 | i18n 双字典不对等、工具函数对畸形输入抛异常、视图/历史状态机错误 |
| **L4** | 端到端流程 | Playwright 模拟真实点击 | — | 计算跑不通、结果落错位置、历史回填失效、弹窗校验缺失、active 视图实际不可见 |
| **L5** | 布局 / 响应式 / a11y | 三档视口（桌面 / 平板 / 手机）+ 计算样式 | — | 横向溢出、移动端热区 <44px、按钮无可读名、对比度不足 |

**层间不共享断言**：同一件事在静态层与浏览器层各测一次（如 i18n 覆盖）。静态测「源码有没有写」，浏览器测「运行时有没有生效」，两者各能抓到对方漏掉的情况。

当前规模：**L1=16 · L2=43 · L3=20 · L4=18 · L5=13，合计 110 例**，全量约 70 秒。

---

## 三、如何运行

```bash
cd workbench/autotest

python run_all.py                # 全量 5 层（约 70 秒），产出报告
python run_all.py --layer L1 L3  # 只跑指定层（开发迭代最快）
python run_all.py --keep-report  # 保留本轮报告目录

# 单跑某一层（开发时最快，带详细回溯）
python -m pytest tests/test_L2_api.py -q --tb=short
```

产物落在 `autotest/report/<时间戳>/`：

| 文件 | 内容 |
|---|---|
| `summary.md` | 人读总览（分层通过率 + 失败清单） |
| `failures.md` | 仅失败项的完整回溯 |
| `junit_L*.xml` | 机读明细（CI 集成） |

**环境要求**：Anaconda Python（`C:\Tools\anaconda3\python.exe`，与技能其余脚本一致）；`pip install pytest playwright requests`；`playwright install chromium`。L2/L4 默认以 `CTSS_COZE_MOCK=1` 起后端（验证参数校验 / 响应契约 / 前端渲染，**不验证真实 R 数值**——数值正确性由 `tests/test_ct_samplesize.py` 等方法级测试负责）。

---

## 四、回归基线（本流程守护的 7 个真实 bug）

这些是已发现并修复、且本套件**持续守护不再复发**的问题。改任何相关代码前先读一遍，避免重蹈覆辙：

| # | 层 | 级别 | 问题 | 修复 |
|---|---|---|---|---|
| 1 | L1/L3/L4 | **P0** | `#v-domain` 少一个 `</div>`，「历史记录」视图与页脚被嵌进域视图内部；切到历史页后父级 `display:none`，页面宽高 0，功能完全不可用（不报错，肉眼审代码极难发现） | 补闭合标签，删除残留空 `<div class="sectip">` |
| 2 | L2 | **P0** | 静态资源根即技能根，`/config/llm_key.py`、`/adapters/coze_token_embedded.py` 可被任意 GET 下载（混淆≠加密，密钥与密文同文件） | 静态伺服改为「扩展名白名单 + 目录黑名单 + 文件名黑名单」（`_static_allowed()`） |
| 3 | L2 | **P1** | argparse 校验失败把完整 usage（约 4KB）打到 stderr；云端容器 stderr 常重定向到无人消费的管道，缓冲满则请求永久挂起、并发闸不释放（表现：点计算一直转圈） | `build_namespace()` 用 `redirect_stderr` 收进内存，只回传最后一行精简错误 |
| 4 | L2 | P1 | `survival` 的 optional 里写了 CLI 别名 `hr`，argparse 实际参数是 `hazard_ratio`，名字在 params 中查不到 → 前端渲染出无标签空控件 | `form_schema` 生成 catalog 时按 params 过滤 optional（与 required 同口径） |
| 5 | L3 | P2 | 切 EN 后残留中文：能力域标题「全部方法」（JS 动态写入，`localize()` 覆盖不到）、会话下拉「N 轮 / turn」（en 字典 `turn` 被误填中文） | 抽 `refreshDomainTitle()` 并在 `setLang()` 重放；`setLang()` 增加 `refreshSessions()`；修正 en 字典 |
| 6 | L1 | P2 | `title="切换语言"`、`aria-label="关闭"` 无 i18n 覆盖 | 补 `data-i18n-title/aria` + 双语 key |
| 7 | L5 | P2 | 移动端主 CTA `#nlComputeBtn` 高 40px（ID 选择器特异性高于响应式 `.btn{44px}`），侧栏项 42px | 媒体查询内补同特异性覆盖 |

---

## 五、已知限制与强制护栏

- **mock 模式只验证契约，不验证数值**：L2/L4 用 `CTSS_COZE_MOCK=1`。真实 R 计算数值正确性由 `tests/test_ct_samplesize.py` 等负责，本套件不重复覆盖。
- **🔴 跑 `build_publish.py` 前必须先备份 appId 认领标记**：其 PRUNE 逻辑会剪掉 `publish/.wbapp_*.genie` 与 `publish/.workbuddy/applications.yaml`。丢失后再发布会生成带后缀的新域名，无法回到 `https://ct-samplesize.app.workbuddy.host/`。（权威副本在 `publish-kit/`；丢失后从 `publish-kit/` 拷回并重建 `applications.yaml`。）
- **发布后线上回归**：发布上线后，用真实 `https://ct-samplesize.app.workbuddy.host/` 走一遍 L4 主流程（选方法→填参→计算→历史→导出），确认线上跑的就是这份代码；L2 的凭据白名单与限流在该环境为生产阈值，本套件 `test_rate_limit_actually_works` 已用 `WG_STRICT` 专门验证限流仍生效。
- **测试默认放宽 WebGuard 限流**（`WG_RELAXED`，仅测试进程生效）；限流本身由独立 `WG_STRICT` 实例验证，避免豁免掩盖真实问题。
- **后端子进程 stdout/stderr 必须持续 drain**：`ServerHarness` 用后台线程 drain 到有界 deque，否则 argparse 的 usage 输出会阻塞请求（见 Bug #3）。
- **端口探测禁用 `SO_REUSEADDR`**：Windows 上监听 socket 设了它会误判「已占用=空闲」，新实例 bind 到旧实例端口，请求被旧实例吃掉（表现：断言莫名其妙全绿）。`_free_port()` 已修并注释。
- **副作用文件自动还原**：`sessions.json` / `bugreports.json` 夹具启动时备份、结束时还原，测试不污染真实会话数据。

---

## 六、维护者须知

- 新增检验方法：在 `form_schema.py` 的 catalog 里登记后，L2 的 `param_factory` 会**自动**按 schema 生成合法参数用例，无需手改测试。
- 改 i18n：`zh` / `en` 双字典必须同步；L3 的「双字典 key 对等」用例会抓缺失。
- 改布局：补完 CSS 后跑 L5，确认 375px 视口下无横向溢出、主 CTA ≥44px。
- 套件自身改动后，跑一遍 `run_all.py` 确认全绿再提交；报告落 `autotest/report/`。
- 本流程不进工作台发布载荷（载荷为白名单构建，`autotest/` 不在白名单内），仅随技能源码（GitHub / ClawHub）分发。
