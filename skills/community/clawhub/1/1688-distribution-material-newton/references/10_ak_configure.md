# AK 配置

## 触发条件

- skill 首次触发时必须先检查 AK 是否已配置
- 用户主动要求配置 AK
- 其他命令返回 "AK 未配置" 或 "签名无效" 错误

## 检查 AK 状态

```bash
python3 {baseDir}/cli.py configure
```

- **输出 "✅ AK 已配置"**：直接进入后续步骤，不要向用户提及此检查。
- **输出 "❌ 尚未配置 AK"**：输出 AK 引导话术，然后**停止，等待用户回复，不要做任何其他操作**。

## AK 引导话术

```text
需要先配置 AK，获取方式：
打开 [clawhub.1688.com](https://clawhub.1688.com) 点击右上角**钥匙🔑图标**获取 AK
获取后告诉我：「我的AK是 xxxxxx」
```

## 配置 AK

用户回复 AK 后，从消息中提取 AK 字符串，执行：

```bash
python3 {baseDir}/cli.py configure <提取到的AK>
```

- 配置完成后，直接继续执行用户最初的需求，无需额外说明。

## 异常处理

| 场景 | Agent 应对 |
|------|-----------|
| configure 输出 success=false | 原样输出 markdown 错误信息 |
| 配置成功但后续命令仍报 AK 未配置 | 提示用户新开会话或执行 `openclaw secrets reload`，必要时再重试 configure |
| 用户问"我的 AK 在哪" | 输出上方 AK 引导话术 |
