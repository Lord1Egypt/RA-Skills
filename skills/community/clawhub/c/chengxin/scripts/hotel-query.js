#!/usr/bin/env node

/**
 * 同程程心大模型 - 酒店专用查询 API
 * 
 * 用法：
 *   node hotel-query.js --destination "上海"
 *   node hotel-query.js --destination "上海" --extra "明天入住"
 *   node hotel-query.js --destination "上海" --extra "外滩附近 明天入住"
 *   node hotel-query.js --destination "上海" --extra "最便宜"
 *   node hotel-query.js --destination "上海" --extra "五星级 含早餐"
 * 
 * 参数说明：
 *   --destination <城市>      目的地城市
 *   --extra <补充信息>        额外信息（日期、位置偏好、价格偏好、星级/设施偏好等）
 *   --channel <渠道>          通信渠道（webchat/wechat 等）
 *   --surface <界面>          交互界面（mobile/desktop/table/card）
 * 
 * 配置（优先级：环境变量 > config.json）：
 *   - CHENGXIN_API_KEY（环境变量）
 *   - 或创建 config.json 文件（见 config.example.json）
 */

const { create_query_runner } = require('./lib/base-query');
const { NO_MATCH_DETAIL, MORE_CHOICES_PROMPT } = require('./lib/query-response');
const { format_hotel_card, format_hotel_table } = require('./lib/formatters');

// 酒店 API 路径
const HOTEL_API_PATH = '/hotelResource';

/**
 * 验证参数组合
 * @param {object} params - 参数对象
 * @returns {object} - { valid: boolean, error: string }
 */
function validate_params(params) {
  if (params.destination) {
    return { valid: true };
  }
  
  return { 
    valid: false, 
    error: `⚠️ 参数不完整，请提供目的地城市。
  示例：--destination "上海"`
  };
}

/**
 * 格式化酒店结果
 * @param {object} hotel_data - 酒店数据
 * @param {boolean} use_table - 是否使用表格格式
 * @param {boolean} use_plain_link - 是否使用纯文本链接（转发给底层格式化函数）
 * @returns {string} - 格式化输出
 */
function format_hotel_result(hotel_data, use_table = false, use_plain_link = false) {
  if (!hotel_data || !hotel_data.hotelList) {
    return '未找到相关酒店信息';
  }
  
  const hotels = hotel_data.hotelList;
  let output = '🏨 酒店查询结果：\n\n';
  
  if (use_table) {
    output += format_hotel_table(hotels, use_plain_link);
  } else {
    hotels.forEach((hotel) => {
      output += format_hotel_card(hotel, use_plain_link);
    });
  }
  
  output += MORE_CHOICES_PROMPT;
  output += '\n';
  return output;
}

/**
 * 处理查询结果
 */
function handle_result(response_data, { print_success_once, format_options, print_no_match }) {
  const { use_table, use_plain_link } = format_options;
  const hotel_data_list = response_data?.hotelDataList;

  if (Array.isArray(hotel_data_list) && hotel_data_list.length > 0) {
    let has_output = false;
    hotel_data_list.forEach((item, index) => {
      if (item.hotelList && item.hotelList.length > 0) {
        print_success_once();
        if (item.desc) {
          console.log(`📌 ${item.desc}\n`);
        } else if (hotel_data_list.length > 1) {
          console.log(`📌 列表 ${index + 1}\n`);
        }
        console.log(format_hotel_result(item, use_table, use_plain_link));
        has_output = true;
      }
    });
    if (!has_output) {
      print_no_match();
    }
  } else {
    print_no_match();
  }
}

// 创建查询运行器
const runner = create_query_runner({
  api_path: HOTEL_API_PATH,
  param_defs: {
    destination: '',
    extra: '',
    channel: '',
    surface: ''
  },
  validate: validate_params,
  handle_result: handle_result,
  no_match_detail: NO_MATCH_DETAIL.HOTEL,
  usage_example: `  node hotel-query.js --destination "上海"
  node hotel-query.js --destination "上海" --extra "明天入住"
  node hotel-query.js --destination "上海" --extra "外滩附近 明天入住"`
});

// 导出函数供其他模块使用
module.exports = {
  validate_params,
  format_hotel_result
};

// 运行主函数
if (require.main === module) {
  runner.run();
}
