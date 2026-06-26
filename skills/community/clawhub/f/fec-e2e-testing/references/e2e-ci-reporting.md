# E2E CI 与报告

## CI 集成（示例）

```yaml
# .github/workflows/e2e.yml
name: E2E Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm ci
      - run: npx playwright install --with-deps
      - run: npx playwright test
        env:
          CI: true
          BASE_URL: ${{ vars.STAGING_URL }}
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 30
```

Cypress：固定 `CYPRESS_baseUrl` 或配置文件中的 `baseUrl`，失败截图/视频同样建议上传 artifact。

## E2E 报告模板（Markdown）

输出或归档测试报告时可采用下列结构，便于复盘：

```markdown
# E2E 测试报告

**日期：** YYYY-MM-DD HH:mm
**耗时：** X 分 Y 秒
**结果：** 通过 / 失败

## 摘要

- 总计 X | 通过 Y | 失败 Z | 不稳定/跳过 说明

## 失败用例

### 用例名

- **文件：** `tests/e2e/xxx.spec.ts:行号`
- **错误：** 简述断言或超时信息
- **截图/Trace：** 路径或 artifact 名称
- **建议修复：** 可执行结论

## 产物

- HTML 报告：`playwright-report/index.html`
- Trace / 视频 / 截图：CI artifact 或本地 `test-results/`
```
