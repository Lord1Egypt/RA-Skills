# 安全、质量与打包清单

## 安全清单

生成 Skill 时必须写入：

- 删除文件前确认
- 覆盖文件前确认
- 发送消息前确认
- 发布内容前确认
- 付款前确认
- 授权登录前确认
- 读取隐私文件前确认
- 不要求用户直接发送密码、验证码、私钥、token

## 质量清单

完成前检查：

- `name` 使用小写英文、数字、连字符
- `description` 说清楚做什么和什么时候触发
- 用户输入说清楚
- 用户输出说清楚
- 工作步骤不超过必要长度
- 新手能看懂 README
- 至少有 3 个测试提问
- 所有引用文件都存在

## 打包清单

应该包含：

- `SKILL.md`
- `README.md`
- `examples.md`
- 必要的 `references/`
- 必要的 `scripts/`
- 必要的 `assets/`

不要打包：

- `.env`
- token、cookie、API key
- `node_modules`
- 缓存文件
- 日志文件
- 临时文件
- 个人隐私文件

## 推荐 manifest

```json
{
  "name": "skill-name",
  "version": "0.1.0",
  "description": "一句话说明",
  "author": "",
  "created_for": "Codex",
  "entry": "SKILL.md"
}
```

