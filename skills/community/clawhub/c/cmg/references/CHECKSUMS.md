# 扫描器发布包校验和 (SHA-256)

下载扫描器二进制后**必须**核对校验和再解压执行。使用 `{baseDir}/scripts/fetch_scanner.sh` 会自动完成校验。

基础地址：`https://msp-release-1258344699.cos.ap-shanghai.myqcloud.com/package/urp/`

> **这些值的含义与局限**：校验和由维护者于 **2026-08-12** 从上述 COS 地址实际下载各文件计算得出，
> 记录的是当时发布产物的状态。它能检测出此后文件被替换、损坏或中间人篡改，
> 但**不能**证明原始产物本身可信 —— 上游未提供签名或官方校验和清单。
> 若校验失败，不要继续执行，请先向维护者确认。

| 文件 | 大小 | SHA-256 |
| --- | ---: | --- |
| `aliyun-scanner-linux-1.0.0.tar.gz` | 73.9 MB | `6d8c86f454630c5d4e079066d9a217c401346d0780616f5dc1178cf04fea10ab` |
| `aliyun-scanner-mac-amd64-1.0.0.tar.gz` | 76.0 MB | `2399e684fb509e14b83f71f252cf2b58c59150d7fdb73ad43ea758c595447579` |
| `aliyun-scanner-mac-arm64-1.0.0.tar.gz` | 69.4 MB | `179c80e7737fc6979a9c0187a66615bc8a5c4d462f599d1a5f6e752c2b8a79c7` |
| `aliyun-scanner-win-amd64-1.0.0.zip` | 0.0 MB | `1ffade0549a4ff019d095cea4aedba0b51a18357a459e841ce36484c323b6e3c` |
| `aws-scanner-linux-1.0.0.tar.gz` | 16.9 MB | `5f1d60443dec7812e95a16e2703f02d9e32b1ad14da9846079e4837043fc5088` |
| `aws-scanner-linux-zh-1.0.0.tar.gz` | 45.7 MB | `9c1d26569bfdca8cc4ab90c5f82cc4a46655fb325f4df6cbc32672b8b003f293` |
| `aws-scanner-mac-amd64-1.0.0.tar.gz` | 17.4 MB | `be91b6ca49e5bf9293b424e3b1e7524eb555dbe12eb0fae146e5be574bfcdc8c` |
| `aws-scanner-mac-amd64-zh-1.0.0.tar.gz` | 46.9 MB | `58aa06e9972f33726def49683ab95a411339fe8c3ddee42af6ae77e127e5ece0` |
| `aws-scanner-mac-arm64-1.0.0.tar.gz` | 16.0 MB | `895980f5e202985bdcb80cbb20c51e327120bb3e3fde991054e4f26a333ceb71` |
| `aws-scanner-mac-arm64-zh-1.0.0.tar.gz` | 42.3 MB | `ba936da58877c128d6a9082338a3947eabe8d613de9037cc40610e734a7037c3` |
| `aws-scanner-win-amd64-zh-1.0.0.zip` | 46.5 MB | `6306efa5436fcfa94e09a2bba9c79cddab4574ece357c90bfb6e857f26e2566b` |
| `huaweicloud-scanner-linux-1.0.0.tar.gz` | 53.6 MB | `0647216bc8406ac4e653918d9df19143de4c6569274fc33ae4103342e5550275` |
| `huaweicloud-scanner-mac-amd64-1.0.0.tar.gz` | 55.1 MB | `f2056e51294467731da8d05c2fbe9abe8e0b2c0c2b4f0ffda6afc0823241d2db` |
| `huaweicloud-scanner-mac-arm64-1.0.0.tar.gz` | 50.4 MB | `f5b107caf40d9fffc21ce60e414417f73471f1d550a9078c5bce1bcaeadeb32c` |
| `huaweicloud-scanner-win-amd64-1.0.0.zip` | 54.7 MB | `db2f3ce37144b6f55b3215928db5d74e2a97060d667f5cc5c083a11e5a4963bd` |

## 已知不可用的产物

以下产物在 `scan.md` 中被列出，但实际不可用，**不要引导用户下载**：

| 文件 | 问题 |
| --- | --- |
| `aws-scanner-win-amd64-1.0.0.zip` | 返回 HTTP 404，产物不存在 |
| `aliyun-scanner-win-amd64-1.0.0.zip` | 仅 1,955 字节，压缩包内只有 `ReadMe.txt` 与 `config.yaml`，缺少扫描器可执行文件 |

Windows 用户请改用华为云 / AWS 国内站产物，或在 Linux / macOS 环境下执行扫描。
