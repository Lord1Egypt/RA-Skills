async function BASE() { const d = await chrome.storage.local.get("serverUrl"); const u = (d.serverUrl || "").trim(); return u ? u.replace(/\/$/, "") : "http://127.0.0.1:17890"; }
async function AUTH() { const d = await chrome.storage.local.get("apiToken"); const t = (d.apiToken || "").trim(); return t ? { "Authorization": "Bearer " + t } : {}; }

const $ = (id) => document.getElementById(id);

async function main() {
  const d = await chrome.storage.local.get(["serverUrl", "apiToken"]);
  $("serverUrl").value = d.serverUrl || "http://127.0.0.1:17890";
  $("apiToken").value = d.apiToken || "";
  const capState = await chrome.storage.local.get({ captureDownloads: true });
  $("captureDownloads").checked = capState.captureDownloads;
  $("captureDownloads").addEventListener("change", async () => {
    await chrome.storage.local.set({ captureDownloads: $("captureDownloads").checked });
  });
  $("saveServer").addEventListener("click", async () => {
    const serverUrl = $("serverUrl").value.trim().replace(/\/$/, "");
    await chrome.storage.local.set({ serverUrl, apiToken: $("apiToken").value.trim() });
    $("serverMsg").textContent = "✅ 已保存";
    setTimeout(() => $("serverMsg").textContent = "", 1600);
  });
  $("tstart").addEventListener("click", async () => {
    const url = ($("url").value || "").trim().split(/\s+/).find((x) => /^https?:\/\//i.test(x)) || "";
    if (!url) { setStatus("先粘贴链接再测试", "err"); return; }
    const qs = new URLSearchParams({ url });
    const tpwd = ($("tpwd").value || "").trim();
    if (tpwd) qs.append("pwd", tpwd);
    try {
      const resp = await fetch(await BASE() + "/api/test?" + qs.toString(), { headers: await AUTH() });
      const data = await resp.json();
      if (!data || !data.checks) { $("tres").innerHTML = "<span class='err'>测试失败：" + ((data && data.error) || "未知") + "</span>"; return; }
      let html = "";
      let allOk = true;
      (data.checks || []).forEach((c) => { if (!c.ok) allOk = false; html += `<div>${c.ok ? "✅" : "❌"} ${c.name}：${c.detail || ""}</div>`; });
      $("tres").innerHTML = `<div class="${allOk ? "ok" : "err"}">${allOk ? "✅ 可以开始下载" : "❌ 还不能直接下载"}</div>` + html;
    } catch (err) {
      $("tres").innerHTML = "<span class='err'>连接本机失败，请先执行 pan serve</span>";
    }
  });

  $("start").addEventListener("click", async () => {
    const url = ($("url").value || "").trim();
    const body = {
      url: url.split(/\s+/).find((s) => /^https?:\/\//i.test(s)) || "",
      pwd: $("pwd").value.trim(),
      to: $("to").value.trim(),
      engine: $("engine").value,
      tier: $("tier").value,
      path: ""
    };
    if (!body.url) {
      setStatus("请粘贴至少一个网盘链接", "err");
      return;
    }
    try {
      const resp = await fetch(await BASE() + "/api/download", {
        method: "POST",
        headers: Object.assign({ "Content-Type": "application/json" }, await AUTH()),
        body: JSON.stringify(body)
      });
      const data = await resp.json();
      if (data.ok) {
        setStatus("已开始下载 PID " + data.pid + "，可打开任务中心查看进度。", "ok");
        chrome.storage.local.set({ latest: { pwd: body.pwd, to: body.to, engine: body.engine, tier: body.tier, path: "" } });
      } else {
        setStatus("失败：" + (data.error || "未知错误"), "err");
      }
    } catch (err) {
      setStatus("连接失败：请检查插件里的服务地址。", "err");
    }
  });
}

function setStatus(text, cls) {
  const el = $("status");
  el.textContent = text;
  el.className = "status " + (cls || "");
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", main);
} else {
  main();
}
