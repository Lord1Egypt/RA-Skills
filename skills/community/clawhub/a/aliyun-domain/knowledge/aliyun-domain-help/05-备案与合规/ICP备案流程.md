# ICP 备案流程

> **来源**: 阿里云帮助文档  
> **原文地址**: https://help.aliyun.com/zh/icp-filing/basic-icp-service/user-guide/icp-filing-application-overview  
> **更新时间**: 2026-03-16  
> **抓取时间**: 2026-03-16

---

## 📄 文档内容

使用阿里云节点服务器时，可通过阿里云ICP备案系统提交申请，审核通过即可开通网站/App服务。本文介绍备案流程及注意事项。

---

## 阅读前须知

根据《非经营性互联网信息服务备案管理办法》规定，**中国内地服务器必须在服务器所属接入商平台完成备案，否则网站将面临关停风险。海外服务器不需要。**

### 阿里云备案的前提条件

**使用阿里云中国内地服务器**，只有这样，阿里云才能为您备案。

**不符合条件的情况：**
- **用其他厂商服务器？** → 在相应厂商备案
- **用阿里云香港、海外服务器？** → 无需备案

**说明**: 即使您的网站/App 已在工信部完成备案，要在阿里云正常使用，仍然需要在阿里云按照流程完成新增接入的备案。

---

## 备案类型

您无需手动选择您的备案类型。按照备案流程填写您的主办者信息及网站/App信息，阿里云会自动判断您的备案类型并生成订单。

### 主办者未在阿里云备案

- **首次备案**: 主办者和网站/App 第一次进行ICP备案
- **（无主体）新增互联网信息服务**: 主办者已在工信部有备案信息，现有新的网站/App托管到阿里云中国内地节点服务器
- **新增接入**: 主办者已在工信部有备案信息，网站/App在工信部已有备案信息，现需要新增阿里云作为接入服务商

### 主办者已在阿里云备案

- **（有主体）新增互联网信息服务**: 主办者已在阿里云成功备案，现有新的网站/App托管到阿里云中国内地节点服务器
- **新增接入**: 主办者已在阿里云成功备案，网站/App在工信部已有备案信息，现需要新增阿里云作为接入服务商

---

## ICP备案前准备

| 项目 | 说明 | 参考文档 |
|:---|:---|:---|
| **注册阿里云账号** | 用于申请ICP备案和后续维护ICP备案信息。一个阿里云账号最多只能有一个备案主体。 | [注册阿里云账号用于备案主体](https://help.aliyun.com/zh/icp-filing/basic-icp-service/user-guide/create-an-alibaba-cloud-account-to-apply-for-an-icp-filing) |
| **域名准备与检查** | 完成域名注册及域名实名认证，并检查您的域名是否符合ICP备案要求。 | [域名注册快速入门](https://help.aliyun.com/zh/dws/getting-started/quickly-register-a-new-domain-name)<br>[域名准备与检查](https://help.aliyun.com/zh/icp-filing/basic-icp-service/user-guide/prepare-and-check-the-domain-name) |
| **服务器准备** | 通过阿里云备案，需要先准备阿里云中国内地节点服务器。 | [备案服务器检查](https://help.aliyun.com/zh/icp-filing/basic-icp-service/user-guide/icp-filing-server-access-information-check) |
| **ICP备案所需资料** | 主体为个人和单位所需资料不同。 | [ICP备案所需资料](https://help.aliyun.com/zh/icp-filing/basic-icp-service/user-guide/required-materials) |
| **前置审批（可选）** | 新闻类、出版类、药品和医疗器械类、金融、宗教等行业的相关互联网信息服务需办理对应的前置审批手续。 | [前置审批](https://help.aliyun.com/zh/icp-filing/basic-icp-service/user-guide/pre-approvals) |
| **学习管局规则** | 了解ICP备案所在地域的管局规则，根据管局要求准备ICP备案的材料。 | [各地区管局备案规则](https://help.aliyun.com/zh/icp-filing/basic-icp-service/user-guide/icp-filing-regulations-of-the-miit-for-different-regions) |

---

## 备案流程

无论首次备案、接入已有备案、新增其他服务，均需按照以下流程进行：

### 步骤一：填写ICP备案订单

1. **填写基础信息**  
   在 [阿里云ICP代备案管理系统](https://beian.aliyun.com/order/index.htm) 单击**开始备案**，按页面提示填写主办单位信息和网站/App信息，系统会自动校验您是否具备备案条件。

2. **填写主办者信息**  
   填写ICP备案主办单位的真实信息。

3. **填写网站或App的信息**  
   - 网站：填写网站信息、网站/App 的接入信息
   - App：填写 App 信息、网站/App 的接入信息、App 特征信息

4. **上传资料及真实性核验**  
   按页面提示上传所需资料并完成真实性核验。

5. **信息确认**  
   ICP备案申请提交前，请仔细核对主体、网站或App等所有备案信息，确认无误后提交订单。

### 步骤二：阿里云初审

提交ICP备案申请后，阿里云审核专员会在**1～2个工作日**完成初审并反馈结果，通过后将自动提交至管局审核。

### 步骤三：工信部短信核验

进行ICP备案申请时需通过 [工信部备案管理系统](https://beian.miit.gov.cn) 进行短信核验。

### 步骤四：管局审核

短信核验完成后，管局进行最终审核。审核通过后备案完成，结果将发送至您的手机和邮箱。可登录 [阿里云ICP代备案管理系统](https://beian.aliyun.com/order/index.htm) 查看ICP备案进度。

### 步骤五：ICP备案后处理

| 项目 | 说明 | 参考文档 |
|:---|:---|:---|
| **开通网站或App** | 备案成功后即可开通网站或APP。将ECS公网IP绑定域名并完成解析，即可通过域名访问网站。 | [添加解析记录](https://help.aliyun.com/zh/dns/add-a-dns-record) |
| **添加ICP备案号等信息** | **网站要求**：在首页底部添加备案号，并设置跳转至工信部的链接。<br>**App要求**：在"设置"或"介绍"等显著位置标注备案编号。<br>**特殊要求**：部分省份要求在互联网信息服务下方添加版权所有。 | [添加ICP备案号和版权处理](https://help.aliyun.com/zh/icp-filing/basic-icp-service/the-icp-record-post-processing-1) |
| **公安联网备案** | 依据《计算机信息网络国际联网安全保护管理办法》，网站/App开通后30天内必须完成公安备案。 | [公安联网备案快速入门](https://help.aliyun.com/zh/icp-filing/basic-icp-service/quick-start-for-public-security-network-filing-for-personal-websites) |
| **ICP许可证（可选）** | **适用范围**：经营性网站或App（向用户提供有偿信息或服务）需要申请。<br>**办理时机**：ICP备案完成后即可申请经营性ICP许可证。 | [经营性备案](https://help.aliyun.com/zh/icp-filing/basic-icp-service/business-for-the-record) |

---

## 常见问题

- 若您在原万网备案平台下存在ICP备案信息，现需在阿里云备案，请 [认领原万网ICP备案](https://help.aliyun.com/zh/icp-filing/basic-icp-service/user-guide/to-claim-the-original-nets-icp-for-the-record)
- **备案场景及概念** 常见问题参见：[备案场景及基本概念FAQ](https://help.aliyun.com/zh/icp-filing/basic-icp-service/support/faq-about-icp-filing-preparations)
- **备案流程** 常见问题参见：[备案流程FAQ](https://help.aliyun.com/zh/icp-filing/basic-icp-service/support/for-the-record-process-faq)
- **备案域名** 常见问题参见：[备案域名注意事项](https://help.aliyun.com/zh/icp-filing/basic-icp-service/support/for-the-record-domain-faq)
- **备案账号** 常见问题参见：[备案账号FAQ](https://help.aliyun.com/zh/icp-filing/basic-icp-service/support/for-the-record-account-maintenance-faq)
- **备案驳回** 常见问题参见：[备案驳回FAQ](https://help.aliyun.com/zh/icp-filing/basic-icp-service/support/for-the-record-to-dismiss-the-faq)
- **备案信息** 常见问题参见：[备案信息专项核查 FAQ](https://help.aliyun.com/zh/icp-filing/basic-icp-service/support/for-the-record-information-special-verification-faq)
- **不同场景** 常见问题参见：[不同场景下的ICP备案说明FAQ](https://help.aliyun.com/zh/icp-filing/basic-icp-service/product-overview/faq-about-icp-filing-applications-in-different-scenarios)

---

## 🔗 相关链接

- [阿里云ICP代备案管理系统](https://beian.aliyun.com/order/index.htm)
- [工信部备案管理系统](https://beian.miit.gov.cn)
- [域名准备与检查](https://help.aliyun.com/zh/icp-filing/basic-icp-service/user-guide/prepare-and-check-the-domain-name)
- [备案服务器检查](https://help.aliyun.com/zh/icp-filing/basic-icp-service/user-guide/icp-filing-server-access-information-check)
- [ICP备案所需资料](https://help.aliyun.com/zh/icp-filing/basic-icp-service/user-guide/required-materials)
- [各地区管局备案规则](https://help.aliyun.com/zh/icp-filing/basic-icp-service/user-guide/icp-filing-regulations-of-the-miit-for-different-regions)

---

*本文档由自动化脚本抓取生成，内容版权归阿里云所有*
