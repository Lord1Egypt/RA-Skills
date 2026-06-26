# 数据处理最佳实践

## 站点类型识别

| 站点类型 | 特征 | 推荐工具 |
|----------|------|----------|
| 静态页面 | HTML直接输出 | requests+BeautifulSoup |
| 动态渲染 | JS加载内容 | Playwright/Selenium |
| API接口 | JSON响应 | requests直接调用 |

## 配置建议

- 使用前先通过 `process-engine.py config` 了解目标站点特征
- 根据站点类型选择合适的处理模式
- 建议添加适当的延迟，避免对目标站点造成压力
