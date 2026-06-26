---
name: axios-supply-chain-attack-check
description: "针对axios@1.14.1/0.30.4恶意投毒事件，提供1分钟快速排查脚本，适用于所有前端项目。"
source:https://mp.weixin.qq.com/s/UP7_LLilOOgZPVW8tCsNrg?from=groupmessage&scene=1&subscene=10000&clicktime=1774932741&enterid=1774932741&sessionid=0&ascene=1&realreporttime=1774932741992&forceh5=1
author: gaoguoqing
---

# Skill Instructions

## 适用场景

适用于所有前端项目，当检测到前端项目依赖存在axios恶意版本（1.14.1/0.30.4）、plain-crypto-js@4.2.1后门依赖，或出现开发/构建环境异常外联、未知脚本执行时，立即执行本技能完成应急处置。

---

## 紧急排查

### 依赖版本风险核查及处理

执行以下命令检查项目依赖树中是否存在风险版本：

```bash
bash ./scripts/check-axios-risk.sh

```
