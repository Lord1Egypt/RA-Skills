---
name: china-ecommerce-customer-service
description: 中国电商客服话术生成器。Use when user needs customer service scripts for Taobao, JD, Pinduoduo. Supports inquiry replies, complaint handling, after-sales service, review responses. 淘宝客服、京东客服、拼多多客服、客服话术。
version: 1.0.0
license: MIT-0
metadata: {"openclaw": {"emoji": "💬", "requires": {"bins": [], "env": []}}}
---

# 中国电商客服话术生成器

生成淘宝、京东、拼多多客服话术。

## 功能特点

- 💬 **多场景**: 咨询/投诉/售后/评价
- 🛒 **多平台**: 淘宝/京东/拼多多
- 🎯 **专业话术**: 符合平台规范
- 😊 **高情商**: 专业、礼貌、有效
- 🇨🇳 **中文优化**: 符合中国客服风格
- ⚡ **快速生成**: 即时生成话术

## ⚠️ 免责声明

> **本工具生成的话术仅供参考。**
> 不同AI模型能力不同，话术质量可能有差异。
> 重要客户沟通请人工确认。
> 话术需符合平台规范和法律法规。

## 支持的场景

| 场景 | 示例 |
|------|------|
| 咨询回复 | 产品咨询、订单查询 |
| 投诉处理 | 质量问题、服务投诉 |
| 售后服务 | 退换货、维修 |
| 评价回复 | 好评/差评回复 |
| 催付话术 | 未付款提醒 |
| 好评引导 | 引导好评 |

## 使用方式

```
User: "客户说收到商品有质量问题，怎么回复"
Agent: 生成专业的投诉处理话术

User: "帮我写一个差评回复"
Agent: 生成真诚的差评回复

User: "客户问发货时间，怎么回复"
Agent: 生成友好的咨询回复
```

---

## 平台规范

### 淘宝客服规范

- 响应时间：5分钟内
- 禁止词：绝对、保证、假一赔十
- 推荐用语：亲、您好、感谢

### 京东客服规范

- 响应时间：30秒内
- 禁止词：无法保证、可能
- 推荐用语：尊敬的客户、请问

### 拼多多客服规范

- 响应时间：5分钟内
- 风格：更亲切、口语化
- 推荐用语：亲、宝子、感谢理解

---

## Python代码

```python
class CustomerServiceCopywriter:
    def __init__(self):
        self.platforms = {
            'taobao': {'greeting': '亲，您好', 'closing': '感谢您的支持~'},
            'jd': {'greeting': '尊敬的客户您好', 'closing': '感谢您的信任'},
            'pdd': {'greeting': '亲，你好呀', 'closing': '感谢理解~'}
        }
    
    def generate_inquiry_reply(self, platform, question_type, details):
        """生成咨询回复"""
        
        templates = {
            'shipping': {
                'taobao': '亲，您的订单已发货，预计{days}天内到达，请耐心等待哦~',
                'jd': '尊敬的客户，您的订单已发货，预计{days}天送达。',
                'pdd': '亲，已发货啦，大概{days}天到，耐心等等哦~'
            },
            'product': {
                'taobao': '亲，关于{product}，{answer}，还有其他问题随时问我哦~',
                'jd': '关于{product}，{answer}。如有其他问题请随时咨询。',
                'pdd': '亲，{product}的情况是{answer}，还有啥问题直接问哈~'
            },
            'price': {
                'taobao': '亲，{product}目前价格是{price}元，{promotion}~',
                'jd': '{product}当前售价{price}元，{promotion}。',
                'pdd': '亲，{product}现在{price}元，{promotion}~'
            }
        }
        
        template = templates.get(question_type, {}).get(platform, '请稍等，我帮您查询一下。')
        
        return template.format(**details)
    
    def generate_complaint_reply(self, platform, issue_type, solution):
        """生成投诉回复"""
        
        templates = {
            'quality': {
                'taobao': '亲，非常抱歉给您带来不好的体验。关于{issue}，我们可以{solution}，您看可以吗？',
                'jd': '尊敬的客户，对于您遇到的问题我们深表歉意。针对{issue}，我们可以{solution}。',
                'pdd': '亲，真的抱歉让你遇到{issue}的情况。我们可以{solution}，你看行不？'
            },
            'shipping': {
                'taobao': '亲，非常抱歉物流出现问题。{solution}，给您添麻烦了~',
                'jd': '对于物流问题我们深表歉意。{solution}。',
                'pdd': '亲，物流出了问题真的很抱歉。{solution}~'
            }
        }
        
        template = templates.get(issue_type, {}).get(platform, '抱歉给您添麻烦了，我们{solution}。')
        
        return template.format(
            issue=details.get('issue', '这个问题'),
            solution=solution
        )
    
    def generate_review_reply(self, platform, review_type, content):
        """生成评价回复"""
        
        templates = {
            'positive': {
                'taobao': '亲，感谢您的认可和支持！您的满意是我们最大的动力，期待再次为您服务~',
                'jd': '感谢您的认可，我们会继续努力为您提供更好的服务！',
                'pdd': '谢谢亲的好评！你的支持是我们前进的动力，欢迎下次再来~'
            },
            'negative': {
                'taobao': '亲，非常抱歉给您带来不好的体验。关于您提到的{issue}，我们已经{solution}，希望能得到您的谅解。',
                'jd': '对于您的不满我们深表歉意。针对{issue}，我们已{solution}，感谢您的反馈。',
                'pdd': '亲，真的不好意思让你有{issue}的体验。我们已经{solution}，希望能弥补~'
            }
        }
        
        template = templates.get(review_type, {}).get(platform, '感谢您的反馈！')
        
        return template.format(**content)

# 使用示例
cs = CustomerServiceCopywriter()

# 咨询回复
reply = cs.generate_inquiry_reply('taobao', 'shipping', {'days': '3'})

# 投诉回复
reply = cs.generate_complaint_reply('taobao', 'quality', '为您换货或退款')

# 评价回复
reply = cs.generate_review_reply('taobao', 'negative', {'issue': '产品问题', 'solution': '为您处理'})
```

---

## 话术示例

### 咨询回复

```
客户：这个商品什么时候发货？

回复（淘宝）：
亲，您好！这款商品预计24小时内发货，届时会有物流信息更新。
如有其他问题随时问我哦~

回复（京东）：
尊敬的客户，该商品预计24小时内发货，届时您可查看物流信息。
如有其他问题请随时咨询。

回复（拼多多）：
亲，这款大概24小时内发，发了会通知你的~
还有啥问题直接问哈~
```

### 差评回复

```
回复（淘宝）：
亲，非常抱歉给您带来不好的体验。
关于您提到的问题，我们已经积极处理，希望能得到您的谅解。
如有其他问题随时联系我们~

回复（京东）：
对于您的不满我们深表歉意。
针对您反馈的问题，我们已采取措施改进。
感谢您的宝贵意见。

回复（拼多多）：
亲，真的不好意思让你有不好的体验。
我们已经处理了，希望能弥补~
```

---

## Notes

- 专注中国电商（淘宝/京东/拼多多）
- 话术需符合平台规范
- 支持中文话术生成
- 高情商、专业、礼貌
