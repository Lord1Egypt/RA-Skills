# 中国效率工具集 (China Productivity Toolkit)

中文环境下的实用效率工具集：快递查询、汇率换算、节假日查询、号码归属地等。

## 触发条件
当用户提到以下需求时自动激活：
- 查快递、快递单号、物流信息
- 汇率查询、货币换算
- 节假日、放假安排、调休
- 手机号归属地、号码查询
- IP归属地、IP地址查询

## 使用方法

### 快递查询
```
/china-toolkit express <快递单号> [快递公司代码]
```
支持：顺丰(SF)、中通(ZTO)、圆通(YTO)、申通(STO)、韵达(YD)、EMS、京东(JD)等

### 汇率查询
```
/china-toolkit rate [金额] <源货币> <目标货币>
```
例：`/china-toolkit rate 100 USD CNY`

### 中国节假日
```
/china-toolkit holiday [年份]
```
返回当年节假日和调休安排

### 手机号归属地
```
/china-toolkit phone <手机号>
```

### IP归属地
```
/china-toolkit ip <IP地址>
```

## 安装
```bash
openclaw skills install china-toolkit
```

## 依赖
本技能使用免费公开API，无需任何密钥配置，开箱即用。

## 技术栈
- Node.js
- 免费公开API（kuaidi100、exchangerate-api、timor.tech等）

## 企业服务
需要企业定制、私有化部署或更多功能？访问 [openclawx.asia](https://openclawx.asia) 获取专业支持。

## 作者
- dxg
- 邮箱: 852621787@qq.com
- GitHub: https://github.com/dxg852621787
- 官网: https://openclawx.asia

## 许可证
MIT - 免费使用
