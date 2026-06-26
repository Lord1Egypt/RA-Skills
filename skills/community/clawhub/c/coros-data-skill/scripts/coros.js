import "dotenv/config";
import axios from "axios";
// https://trainingcn.coros.com/admin/views/activities
// https://teamcnapi.coros.com/activity/query?size=20&pageNumber=1&modeList=&startDay=20260303&endDay=20260307

// ==================== 常量配置 ====================

const COROS_URLS = {
  LOGIN_URL: "https://teamcnapi.coros.com/account/login",
  ACTIVITY_LIST: "https://teamcnapi.coros.com/activity/query",
};

const DEFAULT_HEADERS = {
  authority: "teamcnapi.coros.com",
  accept: "application/json, text/plain, */*",
  "accept-language": "zh-CN,zh;q=0.9",
  "content-type": "application/json;charset=UTF-8",
  dnt: "1",
  origin: "https://t.coros.com",
  referer: "https://t.coros.com/",
  "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
};

// ==================== CorosClient 类 ====================

export class CorosClient {
  /**
   * @param {string} account COROS 账号（邮箱）
   * @param {string} password 已 MD5 加密的密码
   */
  constructor(account, password) {
    this.account = account;
    this.password = password;
    this.accessToken = null;
    this.authedAxios = null;
  }

  /**
   * 登录并获取 accessToken，初始化带鉴权的 axios 实例
   */
  async login() {
    const response = await axios.post(
      COROS_URLS.LOGIN_URL,
      {
        account: this.account,
        accountType: 2,
        pwd: this.password,
      },
      { headers: DEFAULT_HEADERS, timeout: 60000 },
    );

    const accessToken = response.data?.data?.accessToken;
    if (!accessToken) {
      throw new Error("登录失败，请检查账号和密码");
    }

    this.accessToken = accessToken;
    this.authedAxios = axios.create({
      timeout: 240000,
      headers: {
        accesstoken: accessToken,
        cookie: `CPL-coros-region=2; CPL-coros-token=${accessToken}`,
      },
    });

    console.log("✅ 登录成功");
  }

/*
  * 获取跑步活动列表
  * @param {string} startDay 开始日期，格式为 YYYYMMDD
  * @param {string} endDay 结束日期，格式为 YYYYMMDD
*/
  async fetchActivity(startDay="20260303", endDay="20260307") {
    const modeList = "100,101,102,103";
    const url = `${COROS_URLS.ACTIVITY_LIST}?modeList=${modeList}&pageNumber=1&size=100&startDay=${startDay}&endDay=${endDay}`;
    const response = await this.authedAxios.get(url);
    const activitys = response.data?.data?.dataList;

    return activitys;
  }
}
