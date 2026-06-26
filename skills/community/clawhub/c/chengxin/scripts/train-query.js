#!/usr/bin/env node

/**
 * 同程程心大模型 - 火车票专用查询 API
 * 
 * 用法：
 *   node train-query.js --departure "北京" --destination "上海"
 *   node train-query.js --train-number "G1234"
 *   node train-query.js --departure-station "北京南站" --arrival-station "上海虹桥站"
 *   node train-query.js --departure "北京" --destination "上海" --extra "明天 高铁"
 *   node train-query.js --departure "北京" --destination "上海" --extra "最晚"
 *   node train-query.js --departure "北京" --destination "上海" --extra "最早 高铁"
 * 
 * 参数说明：
 *   --departure <城市>        出发地城市
 *   --destination <城市>      目的地城市
 *   --departure-station <站>  出发站
 *   --arrival-station <站>    到达站
 *   --train-number <车次>     车次号
 *   --extra <补充信息>        额外信息（日期、时间偏好、价格偏好、席别偏好等）
 *   --channel <渠道>          通信渠道（webchat/wechat 等）
 *   --surface <界面>          交互界面（mobile/desktop/table/card）
 * 
 * 合法组合：
 *   1. 出发地 + 目的地
 *   2. 车次号
 *   3. 出发站 + 到达站
 * 
 * 配置（优先级：环境变量 > config.json）：
 *   - CHENGXIN_API_KEY（环境变量）
 *   - 或创建 config.json 文件（见 config.example.json）
 */

const { create_query_runner } = require('./lib/base-query');
const { NO_MATCH_DETAIL, MORE_CHOICES_PROMPT, ROUND_TRIP_PROMPTS } = require('./lib/query-response');
const { is_transfer_trip, is_round_trip } = require('./lib/data-utils');
const { format_train_table, format_transfer_trip, format_train_card } = require('./lib/formatters');

// 火车票 API 路径
const TRAIN_API_PATH = '/trainResource';

/**
 * 验证参数组合
 * @param {object} params - 参数对象
 * @returns {object} - { valid: boolean, error: string }
 */
function validate_params(params) {
  const has_departure_dest = params.departure && params.destination;
  const has_train_number = params.train_number;
  const has_stations = params.departure_station && params.arrival_station;
  
  if (has_departure_dest || has_train_number || has_stations) {
    return { valid: true };
  }
  
  const has_partial = params.departure || params.destination || 
                      params.departure_station || params.arrival_station;
  
  if (has_partial) {
    let error = '⚠️ 参数不完整，请提供以下组合之一：\n';
    error += '  1. 出发地 + 目的地（--departure "北京" --destination "上海"）\n';
    error += '  2. 车次号（--train-number "G1234"）\n';
    error += '  3. 出发站 + 到达站（--departure-station "北京南站" --arrival-station "上海虹桥站"）';
    return { valid: false, error };
  }
  
  return { valid: false, error: '请提供查询参数' };
}

/**
 * 格式化火车票结果
 * @param {object} train_data - 火车数据
 * @param {boolean} use_table - 是否使用表格格式
 * @param {boolean} use_plain_link - 是否使用纯文本链接（转发给底层格式化函数）
 * @returns {string} - 格式化输出
 */
function format_train_result(train_data, use_table = false, use_plain_link = false) {
  if (!train_data || !train_data.trainList) {
    return '未找到相关火车票信息';
  }
  
  const trains = train_data.trainList;
  let output = '🚄 火车票查询结果：\n\n';
  
  const direct_trains = trains.filter(t => !is_transfer_trip(t));
  const transfer_trains = trains.filter(is_transfer_trip);
  
  if (use_table) {
    if (direct_trains.length > 0) {
      output += format_train_table(direct_trains, use_plain_link) + '\n';
    }
    
    if (transfer_trains.length > 0) {
      transfer_trains.forEach((train) => {
        output += format_transfer_trip(train, use_plain_link);
      });
    }
  } else {
    direct_trains.forEach((train) => {
      output += format_train_card(train, use_plain_link);
    });
    
    if (transfer_trains.length > 0) {
      transfer_trains.forEach((train) => {
        output += format_transfer_trip(train, use_plain_link);
      });
    }
  }
  
  if (direct_trains.length === 0 && transfer_trains.length === 0) {
    output += '⚠️ 未找到符合条件的火车票，请尝试调整查询条件。\n';
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
  const train_data_list = response_data?.trainDataList;

  if (Array.isArray(train_data_list) && train_data_list.length > 0) {
    let has_output = false;

    train_data_list.forEach((item, index) => {
      if (item.trainList && item.trainList.length > 0) {
        print_success_once();
        if (item.desc) {
          console.log(`📌 ${item.desc}\n`);
        } else if (train_data_list.length > 1) {
          console.log(`📌 列表 ${index + 1}\n`);
        }
        console.log(format_train_result(item, use_table, use_plain_link));
        has_output = true;
      }
    });
    if (!has_output) {
      print_no_match();
    } else {
      if (round_trip) {
        console.log(ROUND_TRIP_PROMPTS.TRAIN);
      }
    }
  } else {
    print_no_match();
  }
}

// 创建查询运行器
const runner = create_query_runner({
  api_path: TRAIN_API_PATH,
  param_defs: {
    departure: '',
    destination: '',
    departure_station: '',
    arrival_station: '',
    train_number: '',
    extra: '',
    channel: '',
    surface: ''
  },
  validate: validate_params,
  handle_result: handle_result,
  no_match_detail: NO_MATCH_DETAIL.TRAIN,
  usage_example: `  node train-query.js --departure "北京" --destination "上海"
  node train-query.js --train-number "G1234"
  node train-query.js --departure-station "北京南站" --arrival-station "上海虹桥站"
  node train-query.js --departure "北京" --destination "上海" --extra "明天 高铁"`
});

// 导出函数供其他模块使用
module.exports = {
  validate_params,
  format_train_result
};

// 运行主函数
if (require.main === module) {
  runner.run();
}
