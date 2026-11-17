# AstraFlow Remote Lab 资源与实测核验说明

本目录收录远程桌面与智能体沙箱实测执行的视觉验证资源与架构说明。

## 实测截图与架构资产

- `novnc-windows-active.png`：实测核验截图。展示在洛杉矶地域（`us-ca`）运行的 Windows Server 2022 英文版 UHost 云主机，通过 RDP 桥接接入 AstraFlow 桌面沙箱并通过浏览器 Web noVNC 实时流式传输的画面。
  - 公网 CDN 托管链接（经过验证，HTTP 200 可访问）：`https://cdn.jsdelivr.net/gh/lijinhongucl-pixel/wb-article-images@main/astraflow-remote-lab/novnc-windows-active.png`
- Web 入口分辨率：默认支持 1920x1080 自适应缩放，且支持剪贴板实时双向同步。
