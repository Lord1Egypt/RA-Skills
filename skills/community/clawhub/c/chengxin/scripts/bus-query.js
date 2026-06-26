#!/usr/bin/env node

/**
 * 同程程心大模型 - 长途汽车专用查询 API
 * 
 * 用法：
 *   node bus-query.js --departure "北京" --destination "上海"
 *   node bus-query.js --departure-station "北京六里桥客运站" --arrival-station "上海长途汽车客运站"
 *   node bus-query.js --departure "北京" --destination "上海" --extra "明天"
 *   node bus-query.js --departure "北京" --destination "上海" --extra "最早"
 *   node bus-query.js --departure "北京" --destination "上海" --extra "下午 最便宜"
 * 
 * 参数说明：
 *   --departure <城市>        出发地城市
 *   --destination <城市>      目的地城市
 *   --departure-station <站>  出发站（精确）
 *   --arrival-station <站>    到达站（精确）
 *   --extra <补充信息>        额外信息（日期、时间偏好、价格偏好等）
 *   --channel <渠道>          通信渠道（webchat/wechat 等）
 *   --surface <界面>          交互界面（mobile/desktop/table/card）
 * 
 * 合法组合：
 *   1. 出发地 + 目的地
 *   2. 出发站 + 到达站
 * 
 * 配置（优先级：环境变量 > config.json）：
 *   - CHENGXIN_API_KEY（环境变量）
 *   - 或创建 config.json 文件（见 config.example.json）
 */

const { create_query_runner } = require('./lib/base-query');
const { NO_MATCH_DETAIL, MORE_CHOICES_PROMPT, ROUND_TRIP_PROMPTS } = require('./lib/query-response');
const { is_transfer_trip, is_round_trip } = require('./lib/data-utils');
const { format_bus_card, format_bus_table, format_transfer_trip } = require('./lib/formatters');

// 长途汽车 API 路径
const BUS_API_PATH = '/busResource';

/**
 * 验证参数组合
 * @param {object} params - 参数对象
 * @returns {object} - { valid: boolean, error: string }
 */
function validate_params(params) {
  const has_departure_dest = params.departure && params.destination;
  const has_stations = params.departure_station && params.arrival_station;
  
  if (has_departure_dest || has_stations) {
    return { valid: true };
  }
  
  const has_partial = params.departure || params.destination || 
                      params.departure_station || params.arrival_station;
  
  if (has_partial) {
    let error = '⚠️ 参数不完整，请提供以下组合之一：\n';
    error += '  1. 出发地 + 目的地（--departure "北京" --destination "上海"）\n';
    error += '  2. 出发站 + 到达站（--departure-station "北京六里桥客运站" --arrival-station "上海长途汽车客运站"）';
    return { valid: false, error };
  }
  
  return { valid: false, error: '请提供查询参数' };
}

/**
 * 格式化长途汽车结果（单个方案）
 * @param {Array} buses - 汽车票列表
 * @param {boolean} use_table - 是否使用表格格式
 * @param {boolean} use_plain_link - 是否使用纯文本链接（转发给底层格式化函数）
 * @returns {string} - 格式化输出
 */
function format_bus_result(buses, use_table = false, use_plain_link = false) {
  if (!buses || buses.length === 0) {
    return '';
  }
  
  let output = '';
  
  const direct_buses = buses.filter(b => !is_transfer_trip(b));
  const transfer_buses = buses.filter(is_transfer_trip);
  
  if (use_table) {
    if (direct_buses.length > 0) {
      output += format_bus_table(direct_buses, use_plain_link);
    }
    if (transfer_buses.length > 0) {
      transfer_buses.forEach((bus) => {
        output += format_transfer_trip(bus, use_plain_link);
      });
    }
  } else {
    if (direct_buses.length > 0) {
      direct_buses.forEach((bus) => {
        output += format_bus_card(bus, use_plain_link);
      });
    }
    if (transfer_buses.length > 0) {
      transfer_buses.forEach((bus) => {
        output += format_transfer_trip(bus, use_plain_link);
      });
    }
  }
  
  output += MORE_CHOICES_PROMPT;
  output += '\n';
  return output;
}

/**
 * 处理查询结果
 */
function handle_result(response_data, { print_success_once, format_options, print_no_match, request_params }) {
  const { use_table, use_plain_link } = format_options;
  const round_trip = is_round_trip(request_params?.extra);
  const bus_data_list = response_data?.busDataList;

  if (Array.isArray(bus_data_list) && bus_data_list.length > 0) {
    let has_output = false;
    bus_data_list.forEach((item, index) => {
      const buses = item.busList;
      if (Array.isArray(buses) && buses.length > 0) {
        print_success_once();
        if (item.desc) {
          console.log(`📌 ${item.desc}\n`);
        } else if (bus_data_list.length > 1) {
          console.log(`📌 列表 ${index + 1}\n`);
        }
        console.log(format_bus_result(buses, use_table, use_plain_link));
        has_output = true;
      }
    });
    if (!has_output) {
      print_no_match();
    } else if (round_trip) {
      console.log(ROUND_TRIP_PROMPTS.BUS);
    }
  } else {
    print_no_match();
  }
}

// 创建查询运行器
const runner = create_query_runner({
  api_path: BUS_API_PATH,
  param_defs: {
    departure: '',
    destination: '',
    departure_station: '',
    arrival_station: '',
    extra: '',
    channel: '',
    surface: ''
  },
  validate: validate_params,
  handle_result: handle_result,
  no_match_detail: NO_MATCH_DETAIL.BUS,
  usage_example: `  node bus-query.js --departure "北京" --destination "上海"
  node bus-query.js --departure-station "北京六里桥客运站" --arrival-station "上海长途汽车客运站"
  node bus-query.js --departure "北京" --destination "上海" --extra "明天"`
});

// 导出函数供其他模块使用
module.exports = {
  validate_params,
  format_bus_result
};

// 运行主函数
if (require.main === module) {
  runner.run();
}
