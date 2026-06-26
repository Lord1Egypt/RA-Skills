# configure（配置 AK）

## 说明

配置访问网关所需的 AccessKey（AK）。

## CLI 调用

```bash
# 写入 AK
python3 cli.py configure YOUR_AK

# 查看当前配置状态
python3 cli.py configure
```

## 输出格式

成功写入：
```json
{
  "success": true,
  "markdown": "AK 已保存: `xxxx****xxxx`\n\n后续由 OpenClaw 配置注入生效...",
  "data": {"configured": true}
}
```

未配置：
```json
{
  "success": false,
  "markdown": "AK 尚未配置\n\n运行: `cli.py configure YOUR_AK`",
  "data": {"configured": false}
}
```

## 注意事项

- AK 来源优先级：环境变量 `ALI_1688_AK` > OpenClaw 配置文件
- 写入后需新开会话或执行 `openclaw secrets reload` 才能使新 AK 生效
- AK 最少 32 位

## userId 说明

- `userId` 由网关根据 AK 签名自动注入（`__userId__`），**无需在调用侧手动传递**
- 只要 AK 配置正确，网关会自动识别买家身份
