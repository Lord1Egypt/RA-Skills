# 源站所有权验证规范（Source Site Ownership Verification）

> 适用于「网站搬迁 / Site Migration」类 Skill 的接入规范。
> 版本：v1.0 ｜ 更新：2026-09-11

---

## 1. 目的与范围

在 Skill 执行任何**源站（source site）数据读取、快照、解析、内容搬运**操作之前，必须先证明调用方对该源域名拥有合法控制权。本规范定义三种标准化的所有权验证方式，防止误迁、劫持他人站点或越权抓取。

**核心原则：下发随机令牌 → 用户在源站控制权层面证明持有 → Skill 自动核对。**

---

## 2. 通用安全规则（所有方式均须遵守）

- 每次验证生成**密码学安全的随机 token**，绑定单次迁移任务，禁止复用固定密钥
- token 须设置**过期窗口**（建议 24–72 小时），超时须重新发起
- 校验成功后记录所有权状态；**在执行搬迁前必须再次轻量复检**（防止验证后域名被转交）
- 全程**可审计**：将验证方式、token 摘要、时间戳、结果写入 Skill 运行日志
- 任一方式通过后即可进入下一步；推荐 **DNS TXT 为主、文件验证为辅、Meta 兜底**

---

## 3. 验证方式一：DNS TXT 记录验证（推荐首选）

### 3.1 原理

在源域名的 DNS 中添加平台生成的唯一 TXT 记录，Skill 通过公共 DNS 查询比对。

### 3.2 流程

1. Skill 生成 `verify_token = secure_random(32字节).hex()`
2. 提示用户在源域名 DNS 添加如下记录：

   ```
   记录类型：TXT
   主机/名称：@ （或 _migrate-verify）
   值：<verify_token>
   TTL：建议 600（10 分钟），便于快速生效与清理
   ```

3. Skill 轮询 DNS（如 `dig TXT <domain>` 或 `dns.resolveTxt`）直到命中匹配 token
4. 匹配成功 → 标记所有权验证通过

### 3.3 适用与优点

- ✅ 不依赖源站 Web 服务在线，搬迁前/中/后均稳定
- ✅ 只需域名解析权限，无需服务器文件权限
- ✅ 抗篡改性强，最适合自动化校验

### 3.4 注意事项

- 需处理 **DNS 传播延迟**（轮询间隔建议 30s，总超时 30–60 分钟）
- 验证完成后应提示用户**删除该 TXT 记录**以清理痕迹
- 对仅能修改根目录、无 DNS 权限的用户，退回方式二

---

## 4. 验证方式二：根目录验证文件（HTTP 文件校验）

### 4.1 原理

在源站**网站根目录**放置指定验证文件，Skill 通过 HTTP GET 比对内容。

### 4.2 流程

1. Skill 生成 `verify_token`
2. 提示用户在源站**网站根目录**放置验证文件：

   ```
   文件名：migrate-verify-<token>.txt
   位置：网站根目录（如 public_html/、wwwroot/、htdocs/ 等，视服务器配置而定）
   访问地址：http://<domain>/migrate-verify-<token>.txt
   内容：<verify_token> （须与文件名中的 token 一致）
   ```

   > 直接放在网站根目录下即可，无需额外子目录；用户需保证该文件可通过 Web 直接访问。
   > 验证时**仅使用 HTTP，不强制 HTTPS**，以兼容未部署证书或证书已过期的源站。

3. Skill 请求 `http://<domain>/migrate-verify-<token>.txt`，比对响应体
4. 内容一致 → 标记验证通过

### 4.3 适用与优点

- ✅ 对仅有服务器/主机权限、无法改 DNS 的用户友好
- ✅ 校验即时，接入简单

### 4.4 注意事项

- 源站须**公网可达**（80 端口即可），**仅使用 HTTP，不校验 TLS 证书**，避免因源站无证书、证书过期或 HTTPS 重定向异常导致校验失败
- 文件放在**网站根目录**即可，无需额外子目录；注意 CDN、缓存、SPA 路由、index 重定向导致的文件不可访问
- 验证完成后提示**删除该文件**，避免遗留安全痕迹
- 搬迁场景下稳定性弱于 DNS，建议作为**备选方式**

---

## 5. 验证方式三：HTML Meta 标签验证

### 5.1 原理

在源站首页 `<head>` 中插入指定 meta 标签，Skill 抓取首页 HTML 解析校验。

### 5.2 流程

1. Skill 生成 `verify_token`
2. 提示用户在源站**首页 `<head>` 顶部**插入：

   ```html
   <meta name="site-migrate-verify" content="<verify_token>" />
   ```

3. Skill 抓取首页，解析 HTML 提取 meta 的 `content`
4. 内容一致 → 标记验证通过

### 5.3 适用与优点

- ✅ 集成简单，适合有 CMS / 主题编辑权限的场景
- ✅ 无需接触 DNS 或服务器文件系统

### 5.4 注意事项

- 首页改版、缓存刷新、主题/插件更新**容易丢失标签**，可靠性最低
- 抓取时需禁用/穿透 CDN 缓存，确保读到最新内容
- 仅建议作为**兜底方式**，不推荐作为唯一验证手段

---

## 6. 验证方式对比

| 维度 | DNS TXT（推荐） | 根目录文件 | Meta 标签 |
|---|---|---|---|
| 安全强度 | 高 | 中高 | 中 |
| 稳定性（搬迁场景） | 高 | 中 | 低 |
| 所需权限 | 域名 DNS | 服务器文件/主机 | CMS 编辑 |
| 自动化友好度 | 高 | 高 | 中 |
| 推荐角色 | **主选** | 备选 | 兜底 |

---

## 7. 推荐落地流程（状态机）

```
[生成 token]
     ↓
[提示用户选择验证方式] → DNS TXT（默认）/ 文件 / Meta
     ↓
[轮询校验] ──失败/超时──→ [提示重试或换方式]
     ↓ 通过
[记录 ownership_verified=true + 时间戳]
     ↓
[执行快照 / 搬运 / 解析]
     ↓
[执行前复检 token 仍有效] ←── 防验证后被转交
     ↓
[完成搬迁 → 提示清理 token / 文件 / meta]
```

---

## 8. 最小实现示例（伪代码）

```python
import secrets, time, dns.resolver, requests

def generate_token():
    return secrets.token_hex(32)  # 密码学安全随机令牌

def verify_dns(domain, token, timeout=1800):
    """方式一：DNS TXT 验证"""
    expected = f"migrate-verify={token}"
    for _ in range(timeout // 30):
        try:
            answers = dns.resolver.resolve(f"_migrate-verify.{domain}", "TXT")
            if any(expected in r.to_text() for r in answers):
                return True
        except Exception:
            pass
        time.sleep(30)
    return False

def verify_file(domain, token):
    """方式二：根目录文件验证（文件放在网站根目录即可，仅用 HTTP，不校验证书）"""
    url = f"http://{domain}/migrate-verify-{token}.txt"
    try:
        return requests.get(url, timeout=10).text.strip() == token
    except Exception:
        return False

def verify_meta(domain, token):
    """方式三：HTML Meta 标签验证"""
    html = requests.get(f"http://{domain}/", timeout=10).text
    return f'content="{token}"' in html  # 实际应使用 HTML 解析器
```

---

## 9. 检查清单（Skill 接入必读）

- [ ] token 使用 `secrets` 等密码学安全随机源生成，非固定值
- [ ] token 绑定任务且有过期时间
- [ ] 默认优先引导用户使用 DNS TXT 方式
- [ ] DNS 轮询有超时与退避，不无限阻塞
- [ ] 文件/Meta 校验使用 HTTP，不强制 HTTPS（源站可能无证书）
- [ ] 校验通过后、搬迁执行前有复检
- [ ] 完成后提示清理 TXT 记录 / 验证文件 / Meta 标签
- [ ] 验证结果（方式、token 摘要、时间、结果）写入审计日志
- [ ] 三种方式任一通过即放行，失败给出清晰的重试/换方式指引

---

## 结论

网站搬迁 Skill 应采用 **「DNS TXT 为主、根目录文件为辅、Meta 标签兜底」** 的分层验证策略，核心是「随机令牌 + 源站控制权层面证明 + 自动核对」，确保不动生产数据前完成源站所有权安全校验。
