# FAQ — 常见问题与解决方案

本文档记录实际调试中遇到的问题及已验证的解决方案，供 AI 在遇到错误时参考。

## 配置阶段

### Q: config-from-links 报 `RolePermNotAllow (code: 1254302)`

应用没有被添加到多维表格。脚本的错误处理会匹配 `permission denied`、`Forbidden`、`RolePermNotAllow` 三种关键词并给出提示。

**解决：** 引导用户在知识库的多维表格中添加应用（"..." → "更多" → "添加文档应用"），并将权限设置为**"可管理"**（默认"可编辑"权限不足）。

### Q: config-from-links 报 `NOTEXIST (code: 91402)`

配置文件中的 `app_token` 或 `table_id` 无效（可能是占位符或已被删除的表）。

**解决：** 重新运行 `config-from-links`，从真实的知识库多维表格链接重新提取。

### Q: 提示"链接格式不正确"或"必须使用知识库中的多维表格链接"

用户提供了独立的多维表格链接（`/base/` 格式），而不是知识库中的多维表格链接（`/wiki/` 格式）。

**解决：** 引导用户在飞书知识库中创建多维表格，然后复制其知识库链接（格式为 `https://xxx.feishu.cn/wiki/xxxxx`）。不支持使用独立的多维表格。

### Q: 重命名默认字段报 `field validation failed (code: 99992402)`

飞书更新字段 API 要求请求体中包含 `type` 字段，不能只传 `field_name`。

**解决：** 代码中已修复，重命名时带上 `{ field_name: '标题', type: 1 }`。

### Q: 创建数据表后出现多余的"飞书任务"表

每次运行 `config-from-links` 如果之前的表被手动删除或配置丢失，会创建新表。`createTaskTable` 中已有同名检查逻辑，同名表存在时会复用。

**解决：** 如果有残留的空表需要清理，可以用 API 删除：
```bash
node -e "
const { FeishuClient } = require('./scripts/feishu-client');
const c = require('./config/credentials.json');
const client = new FeishuClient(c.app_id, c.app_secret);
client.request('DELETE', '/open-apis/bitable/v1/apps/<app_token>/tables/<table_id>')
  .then(r => console.log(r.code === 0 ? '已删除' : r.msg));
"
```

### Q: 旧配置如何迁移到新版本？

旧版本使用两个 URL（多维表格 URL + Wiki 文档 URL）的配置方式已废弃。

**解决：** 重新运行 `config-from-links`，只提供知识库中的多维表格链接即可。系统会自动：
1. 提取多维表格信息和知识库 space_id
2. 在多维表格节点下自动创建 "{表名}-任务文档" 作为新的任务文档根节点
3. 更新配置文件

旧的月/日/任务文档仍然可以访问，只是不会作为新任务的父节点。

## 运行阶段

### Q: `validate.js` 卡在最后的清理确认

`validate.js` 结束时会用 `readline` 询问是否删除测试数据，在非交互环境下会挂起。

**解决：** 用 `echo "n" |` 管道自动回答：
```bash
echo "n" | node scripts/validate.js config/credentials.json
```

### Q: 创建文档时报错但任务记录已创建

`createDoc` 会先查记录再创建知识库节点。如果知识库权限有问题，任务记录已经写入多维表格但文档创建失败。

**解决：** 修复权限后重新运行 `create-doc <record_id>` 即可，不需要重新创建任务。

### Q: `parent_node_token` 配置缺失导致文档创建失败

早期版本的配置不存储 `parent_node_token`，或者存储的是旧的 Wiki 文档节点 token。

**解决：** 重新运行 `config-from-links` 并提供知识库中的多维表格链接，会自动写入新的 `parent_node_token`（指向 "{表名}-任务文档" 节点）。
