import type { Skill, SkillTool, SkillContext, SkillResult } from './types.js';

import {
  daikinDiscoverTool,
  daikinDiscover,
} from './tools/discovery.js';

import {
  daikinListTool,
  daikinList,
  daikinAddTool,
  daikinAdd,
  daikinRemoveTool,
  daikinRemove,
  daikinSetDefaultTool,
  daikinSetDefault,
  daikinUpdateTool,
  daikinUpdate,
} from './tools/devices.js';

import {
  daikinStatusTool,
  daikinStatus,
} from './tools/status.js';

import {
  daikinPowerTool,
  daikinPower,
  daikinModeTool,
  daikinMode,
  daikinTemperatureTool,
  daikinTemperature,
  daikinFanTool,
  daikinFan,
  daikinSwingTool,
  daikinSwing,
  daikinPowerfulTool,
  daikinPowerful,
  daikinEconoTool,
  daikinEcono,
  daikinStreamerTool,
  daikinStreamer,
  daikinHolidayTool,
  daikinHoliday,
} from './tools/control.js';

const tools: SkillTool[] = [
  daikinDiscoverTool,
  daikinListTool,
  daikinAddTool,
  daikinRemoveTool,
  daikinSetDefaultTool,
  daikinUpdateTool,
  daikinStatusTool,
  daikinPowerTool,
  daikinModeTool,
  daikinTemperatureTool,
  daikinFanTool,
  daikinSwingTool,
  daikinPowerfulTool,
  daikinEconoTool,
  daikinStreamerTool,
  daikinHolidayTool,
];

const toolHandlers: Record<string, (params: unknown) => Promise<string>> = {
  daikin_discover: daikinDiscover,
  daikin_list: daikinList,
  daikin_add: daikinAdd,
  daikin_remove: daikinRemove,
  daikin_set_default: daikinSetDefault,
  daikin_update: daikinUpdate,
  daikin_status: daikinStatus,
  daikin_power: daikinPower,
  daikin_mode: daikinMode,
  daikin_temperature: daikinTemperature,
  daikin_fan: daikinFan,
  daikin_swing: daikinSwing,
  daikin_powerful: daikinPowerful,
  daikin_econo: daikinEcono,
  daikin_streamer: daikinStreamer,
  daikin_holiday: daikinHoliday,
};

export default class DaikinAirconSkill implements Skill {
  name = 'daikin-aircon';
  description = 'Control Daikin air conditioners over WiFi';
  version = '1.0.0';

  getTools(): SkillTool[] {
    return tools;
  }

  async executeTool(name: string, params: unknown, _context: SkillContext): Promise<SkillResult> {
    const handler = toolHandlers[name];
    if (!handler) {
      return {
        error: `Unknown tool: ${name}`,
      };
    }

    try {
      const result = await handler(params);
      return { result };
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error);
      return { error: message };
    }
  }
}
