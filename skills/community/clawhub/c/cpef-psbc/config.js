module.exports = {
  // 1. 银行API网关地址
  baseUrl: " ",

  // 2. 认证信息（银行分配）
  merch_id: "", //集团客户号
  signSecret: “”, //证书

  // 3. 接口列表
  api: {
    1001: "/account/balance",  //余额查询
    1002: "/account/hisbalance",	   //历史余额查询
    C002: "/account/payment" //网银审核支付
  }
};