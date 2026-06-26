# 1688 网关接口参考

## 接口列表

| 接口 | 路径 | 说明 |
|------|------|------|
| shop_bind_process | POST /api/shop_bind_process/1.0.0 | 查询/初始化绑店流程 |
| shop_bind_process_update | POST /api/shop_bind_process_update/1.0.0 | 更新绑店流程状态 |
| distribution_tools_shops | POST /api/distribution_tools_shops/1.0.0 | 获取 ISV 工具和绑定店铺 |
| shop_and_tool_info | POST /api/shop_and_tool_info/1.0.0 | 获取已绑定工具和店铺（备选） |

## 认证方式

采用 CSK 签名认证，AK 从以下位置读取（优先级从高到低）：

1. 环境变量 `ALI_1688_AK`
2. OpenClaw 配置文件（路径由 `OPENCLAW_CONFIG_DIR` 环境变量控制，默认 `~/.openclaw`）

AK 格式：`Base64(AccessKeySecret(32位) + AccessKeyID)`

## 请求签名流程

1. 计算 body 的 MD5 并 Base64 编码
2. 构造规范化请求头（x-csk-ak, x-csk-time, x-csk-nonce, x-csk-content-md5, x-csk-version）
3. 拼接签名字符串（Method + ContentMD5 + ContentType + Timestamp + CanonicalHeaders + CanonicalResource）
4. 使用 HMAC-SHA256 + Base64 生成签名
