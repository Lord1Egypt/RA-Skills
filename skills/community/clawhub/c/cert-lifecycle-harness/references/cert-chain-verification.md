---
purpose: 证书链完整性 + 多客户端兼容性核查规则（只对比指纹不足以宣告"已更新"）
loaded_by: SKILL.md §10 脚本产物规范、phases/06 验证章节按需引用
blocking: true
---

# 证书链完整性与多客户端兼容性核查规则

> **核心教训**：续签 / 换 CA 后，**只对比叶子证书指纹不足以宣告"已更新"**。
> 浏览器在 TLS 握手时校验的是**完整证书链**（Full Chain），链条任何一环出问题都会触发
> `NET::ERR_CERT_AUTHORITY_INVALID` / `ERR_CERT_INVALID`，而指纹对比**查不出链条问题**。

---

## 1. 指纹对比的盲区（4 类问题查不出）

| 问题类型 | 指纹对比能否发现 | 后果 |
|---|---|---|
| 中间证书缺失（只给叶子不给 Intermediate） | ❌ 查不出 | 严格客户端直接拒绝；Android、iOS、Linux `curl` 常见报错 |
| 中间证书已过期 | ❌ 查不出 | Android 老版本踩过 Let's Encrypt `DST Root CA X3` 过期坑 |
| 链条顺序颠倒（中间证书放在叶子前面） | ❌ 查不出 | OpenSSL 宽容，但部分 TLS 栈严格拒绝 |
| Root CA 不在某客户端信任库 | ❌ 查不出 | 老 Android / 老 iOS / IoT 设备整片失联 |

---

## 2. 核查维度（L1 协议层 5 项齐全才算完成）

| 维度 | 核查方法 | 合格标准 |
|---|---|---|
| **D1 · 服务器下发链完整性** | `openssl s_client -showcerts -connect host:443` | 叶子 + 中间都下发；通常 ≥ 2 张（Root 不下发为最佳实践） |
| **D2 · 链条顺序正确性** | `Certificate chain` 段逐行看 `s:` `i:` 关系 | 叶子在前，中间在后；每一级 `i:` = 下一级 `s:` |
| **D3 · 中间证书有效期** | 从握手输出切出第 2 张证书 → `openssl x509 -noout -dates` | `notAfter` ≥ 叶子 `notAfter` + 30 天（留缓冲） |
| **D4 · 链条可达公信 Root** | `openssl s_client ... -verify_return_error` 或显式 `-CAfile` | `Verification: OK` / `verify return: 1` |
| **D5 · 多客户端兼容性** | SSL Labs (`https://www.ssllabs.com/ssltest/`) 全客户端矩阵 | 总评 ≥ A；`Trusted` 对主流客户端 ≥ 95% ✓ |

---

## 3. 本机 `Verification: OK` 的作用域边界

```
本机 openssl 返回 OK = 本机 OS 信任库 + OpenSSL 版本 视角下链条合法
≠ Chrome / Safari / Firefox 最新版都信任
≠ Android 7.1 及以下信任
≠ iOS 13 及以下信任
≠ 微信内嵌 WebView（低版本 Android）信任
≠ 老版 IE / IoT 设备信任
```

---

## 4. 不同客户端的信任库更新节奏

| 客户端 | 信任库更新方式 | 风险 |
|---|---|---|
| Chrome / Safari / Firefox 最新版 | 浏览器自带 + 定期更新 | 🟢 低 · 主流 Root 都覆盖 |
| 最新 Android / iOS | 系统更新推送 | 🟢 低 · 随系统升级 |
| Android ≤ 7.1 | 跟随 Google Play Services 有限更新 | ⚠️ 中 · 2020 年后新 Root 可能未覆盖 |
| iOS < 13 | 需系统升级（老设备无法升级） | ⚠️ 中 · 停留在 2018 年信任库 |
| 微信 WebView（低版本 Android 宿主） | 依赖宿主 Android 信任库 | ⚠️ 中 · 广泛存在于下沉市场用户 |
| 老版 IE / 老版 JDK / 企业 IoT | 信任库自 2017 年前停更居多 | 🔴 高 · **必测** |

---

## 5. 强制执行步骤（Phase 5 / Phase 6）

```
Step 1  拉取完整链：
         openssl s_client -servername <host> -connect <host>:443 -showcerts </dev/null > chain.txt

Step 2  核对 D1/D2/D3/D4：
         sed -n '/Certificate chain/,/---/p' chain.txt       # D1 + D2
         grep -c "BEGIN CERTIFICATE" chain.txt               # D1 数量
         awk '/BEGIN/{n++} n==2' chain.txt | openssl x509 -noout -dates  # D3
         grep -E "Verify return code|Verification" chain.txt # D4

Step 3  跑 D5 多客户端矩阵（外部服务，耗时 1-2 min）：
         curl -s "https://api.ssllabs.com/api/v3/analyze?host=<host>&publish=off&all=done"
         或访问 https://www.ssllabs.com/ssltest/analyze.html?d=<host>

Step 4  对比基线（若 Phase 5 Dry-Run 采集了 baseline/L1-tls-handshake.txt）：
         diff baseline/L1-tls-handshake.txt post-change/L1-tls-handshake.txt
         期望：仅叶子证书指纹/有效期变化，链条结构一致
```

---

## 6. 降级路径（当 D5 多客户端矩阵无法执行时）

**场景**：客户环境无法访问 SSL Labs（内网 / 合规限制）

**方案 A · 本机多信任库验证**：
```
openssl s_client ... -CAfile /etc/ssl/certs/ca-bundle.crt   # 系统库
openssl s_client ... -CAfile ./android-ca-bundle.pem        # 下载 Android 信任库
openssl s_client ... -CAfile ./ios-ca-bundle.pem            # 下载 iOS 信任库
```

**方案 B · 客户端抽样**（请用户用不同设备实际访问，看是否告警）：
- Chrome / Safari 最新版
- Android 8 / Android 11
- iOS 14 / iOS 16
- 微信内打开（小程序 WebView 场景必测）

**方案 C · 降级为已知保守结论**：
"本机验证 OK，但未覆盖老客户端兼容性"，
在 L3 交付物风险章节显式留痕。

---

## 7. cert_role 对核查的裁剪

| cert_role | D1-D4 | D5 多客户端 |
|---|---|---|
| `edge`（CDN / WAF 边缘） | ✅ 必查 | ✅ 必查（终端用户视角） |
| `origin`（CDN 回源证书） | ✅ 必查 | ❌ 跳过（只有 CDN 节点访问，不经终端） |
| `internal`（内网 mTLS） | ✅ 必查 | ❌ 跳过（客户端是受控内网节点） |
| `mtls-server` / `mtls-client`（双向 mTLS） | ✅ 必查 + 客户端链额外核查 | 🟡 视客户端范围决定 |

---

## 8. Agent 硬边界

```
✅ 必须做：
- Phase 5 / Phase 6 交付物的 L1 协议层验证**必须包含 D1-D5 全部 5 项**（按 cert_role 裁剪后）
- 指纹对比**只是 D1 的必要条件之一**，不得以"指纹一致"作为"已更新"的充分证据
- Phase 5 Dry-Run 阶段采集 baseline 时必须含 -showcerts 输出（不只是叶子）
- 若环境受限无法跑 D5，必须在 L3 交付物显式声明"多客户端兼容性未验证"

❌ 严禁做：
- 仅凭 openssl x509 -fingerprint 对比就宣告"已更新"
- 将本机 Verification: OK 等同于"所有主流客户端信任"
- 把中间证书过期的历史坑（Let's Encrypt DST Root X3 / Sectigo AddTrust）当作与本次无关
- 换 CA 或变更中间证书品牌后不主动提醒客户"可能引发老 Android/iOS 不信任"
```

---

## 9. 自检对应项

本文件的规则落到自检清单的 **C 类 L1 协议层证书链核查强制项**，
见 `review-guides/self-review-checklist.md` 对应条目，
以及 `phases/06-verify-rollback-playbook.md` 六层验证矩阵 L1 协议层。
