---
name: "fnos-openclaw-autostart"
description: "FnOS OpenClaw 开机自启补丁 + 管理页面开关。修改监控端 server/index.js 和 ui/index.html，实现可开关的开机启动。"
---

# FnOS OpenClaw 开机自启补丁

## 问题

FnOS 应用中心（`trim_app_center`）会在开机时自动启动 OpenClaw 的**监控端**，但**不会自动启动 openclaw-gateway**。用户必须每次在应用面板手动点击「启动」。

本补丁注入自动启动逻辑到监控端，并添加管理页面开关（持久化），让用户能够在界面上启用/禁用开机自启。

## 前置条件

```bash
MONITOR_JS="/vol1/@appcenter/trim.openclaw/server/index.js"
UI_HTML="/vol1/@appcenter/trim.openclaw/ui/index.html"
AUTOSTART_CONF="/vol1/@appdata/trim.openclaw/.autostart"
```

## 步骤

### 1. 验证环境 & 查找注入点

先确认文件存在和当前行号（不同版本行号不同，绝不要硬编码）：

```bash
# 确认文件存在
ls -la "$MONITOR_JS" "$UI_HTML"

# 创建 .autostart（默认启用），这是持久化状态文件
# 如果已存在则保留原值
if [ ! -f "$AUTOSTART_CONF" ]; then
  echo "1" > "$AUTOSTART_CONF"
  echo "Created $AUTOSTART_CONF with default enabled"
else
  echo "$AUTOSTART_CONF already exists: $(cat $AUTOSTART_CONF)"
fi

# 找 autostart 函数定义插入点：startRuntimeReconciler 行
echo "=== 函数定义插入点 ==="
grep -n "startRuntimeReconciler" "$MONITOR_JS"

# 找函数调用插入点：registerBackgroundTaskSafetyHandlers 行
echo "=== 函数调用插入点 ==="
grep -n "registerBackgroundTaskSafetyHandlers" "$MONITOR_JS"

# 找 API 路由插入点：telemetry_default 行
echo "=== API 路由插入点 ==="
grep -n "telemetry_default" "$MONITOR_JS"

# 检查是否已有补丁（避免重复注入）
echo "=== 检查是否已补丁 ==="
if grep -q "AUTOSTART_CONF" "$MONITOR_JS"; then
  echo "已有补丁，跳过注入"
else
  echo "尚无补丁，继续"
fi

# 检查 index.html 尾行
echo "=== 前端注入点 ==="
tail -5 "$UI_HTML"

# 确认 Bun bundle 上下文（是否 ES module，影响 require 用法）
head -1 "$MONITOR_JS"
```

### 2. 备份

```bash
cp "$MONITOR_JS" "${MONITOR_JS}.bak"
cp "$UI_HTML" "${UI_HTML}.bak"
```

### 3. server/index.js — 注入 autostart 逻辑

#### 3.1 插入 autoStartDefaultInstance 函数定义

在 `startRuntimeReconciler()` 行**之前**插入：

```bash
sed -i '/^async function startRuntimeReconciler\|^startRuntimeReconciler()/i\
const AUTOSTART_CONF = "\/vol1\/@appdata\/trim.openclaw\/.autostart";\
async function autoStartDefaultInstance() { try {\
    const autoStartFlag = import.meta.require("fs").existsSync(AUTOSTART_CONF)\
      ? import.meta.require("fs").readFileSync(AUTOSTART_CONF, "utf8").trim()\
      : "1";\
    if (autoStartFlag === "0" || autoStartFlag === "false" || autoStartFlag === "disable") {\
      console.log("[monitor] Auto-start is disabled by " + AUTOSTART_CONF); return;\
    }\
    const instance = ensureDefaultInstance();\
    const runtime = await probeInstanceRuntime(instance);\
    if (runtime.running) { console.log("[monitor] OpenClaw gateway is already running, skipping auto-start"); return; }\
    if (!runtime.installed) { console.log("[monitor] OpenClaw is not installed, skipping auto-start"); return; }\
    console.log("[monitor] Auto-starting OpenClaw gateway on boot...");\
    let port = runtime.port;\
    if (!port) { port = randomPort(); await writeInstancePort(instance, port); }\
    const noopEnqueue = () => {};\
    await startOpenclaw(instance, port, noopEnqueue, null);\
    console.log("[monitor] OpenClaw gateway auto-started successfully");\
  } catch (err) { console.error("[monitor] Auto-start failed:", err); }\
}' "$MONITOR_JS"
```

⚠️ **关键注意事项**：
- Bun bundle 是 ES module 上下文，**必须用 `import.meta.require("fs")`**，不能用 `require("fs")`（会抛 `require is not defined`）
- 如果函数定义行格式不同（如无 `async` 前缀），手动检查后调整 sed 匹配模式

#### 3.2 插入函数调用

在 `registerBackgroundTaskSafetyHandlers()` 行**之后**插入：

```bash
sed -i '/^ *registerBackgroundTaskSafetyHandlers()/a\
autoStartDefaultInstance().catch((err) => {\
  console.error("[monitor] auto-start default instance failed:", err);\
});' "$MONITOR_JS"
```

#### 3.3 插入 API 路由（GET + POST）

在 `telemetry_default` 路由之后插入：

```bash
sed -i '/telemetry_default/a\
app10.get(`${apiBase}\/autostart`, async (c3) => {\
  try {\
    const exists = import.meta.require("fs").existsSync(AUTOSTART_CONF);\
    const val = exists ? import.meta.require("fs").readFileSync(AUTOSTART_CONF, "utf8").trim() : "1";\
    return c3.json({ enabled: val !== "0" && val !== "false" && val !== "disable" });\
  } catch (err) { return c3.json({ enabled: true }, 500); }\
});\
app10.post(`${apiBase}\/autostart`, async (c3) => {\
  try {\
    const body = await c3.req.json();\
    if (body && typeof body.enabled === "boolean") {\
      import.meta.require("fs").writeFileSync(AUTOSTART_CONF, body.enabled ? "1" : "0", "utf8");\
      return c3.json({ ok: true, enabled: body.enabled });\
    }\
    return c3.json({ ok: false, message: "invalid body" }, 400);\
  } catch (err) { return c3.json({ ok: false, message: err.message }, 500); }\
});' "$MONITOR_JS"
```

### 4. ui/index.html — 注入 toggle 脚本

在 `</body>` 之前插入脚本（建议使用 Python 或手动编辑，大型 sed 易错）：

```html
<script>
(function() {
  var API = window.location.origin + '/app/trim-openclaw/api/autostart';
  var wrap = null;
  var enabled = false, loading = false;

  function getWrap() {
    if (wrap) return wrap;
    wrap = document.getElementById('oc-autostart-wrap');
    if (wrap) return wrap;
    wrap = document.createElement('div');
    wrap.id = 'oc-autostart-wrap';
    wrap.style.cssText = 'display:inline-flex;align-items:center;gap:4px;font-size:12px;color:var(--semi-color-text-2,#999);white-space:nowrap;margin-right:6px';
    wrap.innerHTML = '<span>\u5f00\u673a\u81ea\u542f</span><div class="oc-autostart-track" style="position:relative;display:inline-block;width:32px;height:18px;border-radius:9px;cursor:pointer;transition:background .2s,opacity .2s;background:var(--semi-color-border,#d9d9d9);flex-shrink:0"><div class="oc-autostart-thumb" style="position:absolute;top:2px;left:2px;width:14px;height:14px;border-radius:50%;background:#fff;transition:left .2s;box-shadow:0 1px 2px rgba(0,0,0,.2)"></div></div>';

    var track = wrap.querySelector('.oc-autostart-track');
    var thumb = wrap.querySelector('.oc-autostart-thumb');

    function setState(on) {
      enabled = on;
      track.style.background = on ? 'var(--semi-color-primary, #2173df)' : 'var(--semi-color-border, #d9d9d9)';
      thumb.style.left = on ? '16px' : '2px';
      loading = false;
      track.style.opacity = '1';
      track.style.pointerEvents = '';
    }

    track.addEventListener('click', function() {
      if (loading) return;
      loading = true;
      track.style.opacity = '0.5';
      track.style.pointerEvents = 'none';
      fetch(API, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ enabled: !enabled }) })
        .then(function(r) { return r.json(); })
        .then(function(d) { if (d.ok) setState(d.enabled); else setState(enabled); })
        .catch(function() { setState(enabled); });
    });

    fetch(API).then(function(r) { return r.json(); }).then(function(d) { setState(d.enabled); }).catch(function() { setState(true); });
    return wrap;
  }

  function inject() {
    if (!document.getElementById('app')) return;
    if (document.querySelector('#oc-autostart-wrap')) return;

    var containers = document.querySelectorAll('[class*="inline-flex"][class*="shrink-0"][class*="justify-end"]');
    for (var i = 0; i < containers.length; i++) {
      var c = containers[i];
      var p = c.parentElement;
      if (p && p.children.length >= 2) {
        var first = p.children[0];
        if (first && first.textContent.indexOf('OpenClaw \u670d\u52a1') !== -1) {
          c.insertBefore(getWrap(), c.firstChild);
          wrap.style.display = 'inline-flex';
          return true;
        }
      }
    }
    return false;
  }

  function init() {
    if (!inject()) {
      var timer = setInterval(function() { if (inject()) clearInterval(timer); }, 300);
      setTimeout(function() { clearInterval(timer); }, 5000);
    }

    var app = document.getElementById('app');
    if (app) {
      var observer = new MutationObserver(function() {
        if (!document.querySelector('#oc-autostart-wrap')) inject();
      });
      observer.observe(app, { childList: true, subtree: true });
    }
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
</script>
```

> SPA 路由切换时：离开首页 → 卡片 DOM 移除 → toggle 自动消失；切回首页 → MutationObserver 检测到变化 → 重新 `inject()`。

### 5. 验证

```bash
# 确认后端所有插入点
grep -n "AUTOSTART_CONF\|autoStartDefaultInstance\|autostart\|startRuntimeReconciler\|registerBackgroundTaskSafetyHandlers" "$MONITOR_JS"

# 确认前端开关脚本注入
grep -c "oc-autostart-wrap" "$UI_HTML"

# 确认无旧版 require("fs") 残留
grep 'require("fs")' "$MONITOR_JS" || echo "OK: no require('fs') found"

# 确认 .autostart 存在
ls -la "$AUTOSTART_CONF"
```

### 6. 重启监控端生效

FnOS 应用面板停止 → 启动 OpenClaw，或 kill 监控进程：
```bash
ps aux | grep "bun.*server/index.js" | grep -v grep
kill <PID>
```

## 验证

1. 进入管理页面 → 卡片头部"打开OpenClaw"按钮左侧应有「开机自启」开关
2. 默认开启（蓝色），点击可关闭（灰色），加载时半透明
3. 切到其他页面再回来 → 开关重新出现
4. 关机重启 NAS → 开关开启时 gateway 自动启动，关闭时不启动
5. 开关状态持久化（存储在 `$AUTOSTART_CONF`）

## 手动开关（命令行）

```bash
# 关闭
echo "0" > $AUTOSTART_CONF
# 开启
echo "1" > $AUTOSTART_CONF
# 查看状态
cat $AUTOSTART_CONF
```

## 应用更新后重新打补丁

FnOS 应用中心更新时会替换 `server/index.js` 和 `ui/index.html`，补丁会被覆盖。

重新打补丁：
1. 检查备份：`ls -la "$BAK_FILE" "${UI_HTML}.bak"`
2. 重复步骤 1-6
3. 如果备份丢失，使用本 skill 重新完成全部步骤

## 回滚

```bash
cp "${MONITOR_JS}.bak" "$MONITOR_JS"
cp "${UI_HTML}.bak" "$UI_HTML"
# 重启监控端
```

## 关键注意事项

### 技术细节
- **必须用 `import.meta.require("fs")`**：Bun bundle 是 ES module 上下文，`require` 不可用
- **不要乐观更新**：点击开关后等 API 返回成功再翻转，失败则恢复
- **加载态样式**：`opacity: 0.5` + `pointer-events: none`
- `.autostart` 默认 `"1"`（启用），保证向后兼容

### 维护注意
- **不要硬编码行号**：每次更新后 `grep -n` 确认实际行号
- **不要硬编码路径**：开头变量根据实际环境调整
- 不同 FnOS 版本路径可能变化
- Bun bundle 的函数定义格式可能随版本变化，sed 匹配模式需要微调
