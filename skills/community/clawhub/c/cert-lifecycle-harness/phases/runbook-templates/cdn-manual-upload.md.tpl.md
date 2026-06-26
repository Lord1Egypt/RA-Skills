---
type: runbook-template
scope: cdn-manual-upload
purpose: CDN 厂商无自动化入口场景的手工上传流程（控制台步骤指引）
---

# Runbook Template · CDN Manual Upload（无 API 场景）

> 部分 CDN 不提供证书替换 API（常见于老版本或私有化 CDN），需走控制台手工流程。本模板是**步骤指引**而非脚本。

## 前置

- [ ] 客户已在 Phase 5 Dry-Run 阶段用测试证书走通完整控制台流程
- [ ] 客户已截图记录每一步 UI 位置
- [ ] 客户已与 CDN 厂商确认变更窗口（部分厂商会限流或排队）

## 手工流程（通用模板）

1. **登录 CDN 控制台**
   - 账号：`${CDN_ACCOUNT_ID}`
   - 子账号权限确认：具有"证书管理 / 上传 / 绑定"权限

2. **上传新证书**
   - 证书内容（fullchain.pem，含中间证书）
   - 私钥内容（privkey.pem，通过密钥管理系统获取）
   - 证书备注：填写本次变更单号 `${CHANGE_TICKET_ID}`

3. **记录新证书 ID**
   - 厂商会返回一个证书 ID，保存备用

4. **逐个域名替换绑定**
   - 对每个 `${CDN_DOMAIN_N}`：
     - 进入域名配置 → HTTPS 设置
     - 切换证书：从旧证书 ID → 新证书 ID
     - 保存；等待厂商下发生效（通常 5-30 min）

5. **验证（每个域名）**
   - `openssl s_client -servername ${CDN_DOMAIN_N} -connect ${CDN_DOMAIN_N}:443`
   - 查看返回证书指纹是否匹配新证书

6. **观察期**
   - 观察 CDN 控制台的 SSL 握手失败率、4xx/5xx 指标
   - 观察时长：见 `06-verify-rollback-playbook.md §3 等待时长参考表`

## 回滚

- 将绑定切回旧证书 ID（旧证书仍在 CDN 证书库中，未删除）
- **不要**立即删除旧证书，保留到过渡期结束（见 `06-verify-rollback-playbook.md §8`）

## 客户核对点

1. CDN 厂商是否有"灰度发布"能力？（部分厂商支持按百分比切换）
2. 厂商生效延时？（同城 5-10 min / 跨区 30 min）
3. 厂商是否会在证书切换瞬间触发缓存刷新？（影响源站压力）
