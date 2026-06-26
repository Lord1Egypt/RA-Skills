# 浏览器自动化框架

所有子能力执行前，必须先完成浏览器环境选择与初始化。

## 执行方式优先级

按以下顺序选择可用的浏览器操作方式：

1. **技能dumate-browser-use**（最优先）
2. **Playwright CLI**：检测 `playwright-cli` 是否已安装，若未安装则尝试自动安装
3. **其他工具链**：Selenium 脚本或其他可用浏览器驱动
4. **人工引导模式**：以上均不可用时，切换为人工引导（见 [fallback.md](fallback.md)）

## Playwright CLI 安装策略

若 `playwright-cli` 不存在，先尝试安装并验证：

```bash
python3 -m pip install -U playwright-cli
playwright-cli --help
```

- 安装成功 → 继续自动化流程
- 安装失败 → 尝试其他工具链，或进入人工引导模式

## 浏览器初始化

- **模式**：有头模式（headed），便于用户观察执行过程
- **默认入口**：根据任务路由决定，素材管理默认 `https://b2bwork.baidu.com/shop/material/index`，其他任务先进后台主页再导航
