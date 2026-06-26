import type { SkillTool } from '../types.js';
import { getConfig, DeviceNotFoundError } from '../config.js';
import { getDeviceManager } from '../device.js';
import { Appliance } from 'daikin-ts';

function getDeviceParam(config: ReturnType<typeof getConfig>, deviceName?: string, locationId?: string) {
  let targetDevice;
  if (deviceName) {
    targetDevice = config.getDevice(deviceName, locationId);
    if (!targetDevice) {
      const matches = config.findDevicesByName(deviceName);
      if (matches.length > 1) {
        const locations = matches.map(d => 
          d.locationName || d.locationId || 'default'
        ).join(', ');
        throw new Error(`Multiple devices found: "${deviceName}" at ${locations}. Please specify location.`);
      }
      throw new Error(`Device "${deviceName}" not found. Use daikin_list to see available devices.`);
    }
  } else {
    targetDevice = config.getDefaultDevice();
    if (!targetDevice) {
      throw new Error('No device specified and no default device set.');
    }
  }
  return targetDevice;
}

function getDisplayName(device: { name?: string; id: string; locationName?: string; locationId?: string }): string {
  const name = device.name || device.id;
  const location = device.locationName || device.locationId;
  return location ? `${name} (${location})` : name;
}

export const daikinPowerTool: SkillTool = {
  name: 'daikin_power',
  description: 'Turn a Daikin air conditioner on or off.',
  parameters: {
    type: 'object',
    properties: {
      device: {
        type: 'string',
        description: 'Name of the device',
      },
      locationId: {
        type: 'string',
        description: 'Location ID if device name exists in multiple locations',
      },
      power: {
        type: 'string',
        enum: ['on', 'off'],
        description: 'Power state',
      },
    },
    required: ['power'],
  },
};

export async function daikinPower(params: { device?: string; locationId?: string; power: 'on' | 'off' }): Promise<string> {
  const config = getConfig();
  const targetDevice = getDeviceParam(config, params.device, params.locationId);
  const deviceManager = getDeviceManager();
  const device = await deviceManager.getDevice(targetDevice);

  await device.set({ pow: params.power === 'on' ? '1' : '0' });

  return `${getDisplayName(targetDevice)} is now ${params.power.toUpperCase()}.`;
}

export const daikinModeTool: SkillTool = {
  name: 'daikin_mode',
  description: 'Set the operation mode of a Daikin air conditioner.',
  parameters: {
    type: 'object',
    properties: {
      device: {
        type: 'string',
        description: 'Name of the device',
      },
      locationId: {
        type: 'string',
        description: 'Location ID if device name exists in multiple locations',
      },
      mode: {
        type: 'string',
        enum: ['auto', 'cool', 'heat', 'dry', 'fan'],
        description: 'Operation mode',
      },
    },
    required: ['mode'],
  },
};

export async function daikinMode(params: { device?: string; locationId?: string; mode: 'auto' | 'cool' | 'heat' | 'dry' | 'fan' }): Promise<string> {
  const config = getConfig();
  const targetDevice = getDeviceParam(config, params.device, params.locationId);
  const deviceManager = getDeviceManager();
  const device = await deviceManager.getDevice(targetDevice);

  const modeMap: Record<string, string> = {
    auto: '0',
    cool: '3',
    heat: '4',
    dry: '2',
    fan: '6',
  };

  await device.set({ mode: modeMap[params.mode] });

  return `${getDisplayName(targetDevice)} mode set to ${params.mode.toUpperCase()}.`;
}

export const daikinTemperatureTool: SkillTool = {
  name: 'daikin_temperature',
  description: 'Set the target temperature of a Daikin air conditioner.',
  parameters: {
    type: 'object',
    properties: {
      device: {
        type: 'string',
        description: 'Name of the device',
      },
      locationId: {
        type: 'string',
        description: 'Location ID if device name exists in multiple locations',
      },
      temperature: {
        type: 'number',
        description: 'Target temperature in Celsius (10-32, use decimal format like 22.5)',
      },
    },
    required: ['temperature'],
  },
};

export async function daikinTemperature(params: { device?: string; locationId?: string; temperature: number }): Promise<string> {
  const config = getConfig();
  const targetDevice = getDeviceParam(config, params.device, params.locationId);
  const deviceManager = getDeviceManager();
  const device = await deviceManager.getDevice(targetDevice);

  const tempStr = params.temperature.toString();
  await device.set({ stemp: tempStr });

  return `${getDisplayName(targetDevice)} target temperature set to ${params.temperature}°C.`;
}

export const daikinFanTool: SkillTool = {
  name: 'daikin_fan',
  description: 'Set the fan speed of a Daikin air conditioner.',
  parameters: {
    type: 'object',
    properties: {
      device: {
        type: 'string',
        description: 'Name of the device',
      },
      locationId: {
        type: 'string',
        description: 'Location ID if device name exists in multiple locations',
      },
      rate: {
        type: 'string',
        enum: ['auto', 'silence', '1', '2', '3', '4', '5'],
        description: 'Fan speed',
      },
    },
    required: ['rate'],
  },
};

export async function daikinFan(params: { device?: string; locationId?: string; rate: 'auto' | 'silence' | '1' | '2' | '3' | '4' | '5' }): Promise<string> {
  const config = getConfig();
  const targetDevice = getDeviceParam(config, params.device, params.locationId);
  const deviceManager = getDeviceManager();
  const device = await deviceManager.getDevice(targetDevice);

  const fanMap: Record<string, string> = {
    auto: 'A',
    silence: 'B',
    '1': '3',
    '2': '4',
    '3': '5',
    '4': '6',
    '5': '7',
  };

  await device.set({ f_rate: fanMap[params.rate] });

  return `${getDisplayName(targetDevice)} fan speed set to ${params.rate.toUpperCase()}.`;
}

export const daikinSwingTool: SkillTool = {
  name: 'daikin_swing',
  description: 'Set the fan swing mode of a Daikin air conditioner.',
  parameters: {
    type: 'object',
    properties: {
      device: {
        type: 'string',
        description: 'Name of the device',
      },
      locationId: {
        type: 'string',
        description: 'Location ID if device name exists in multiple locations',
      },
      mode: {
        type: 'string',
        enum: ['off', 'vertical', 'horizontal', '3d'],
        description: 'Swing mode',
      },
    },
    required: ['mode'],
  },
};

export async function daikinSwing(params: { device?: string; locationId?: string; mode: 'off' | 'vertical' | 'horizontal' | '3d' }): Promise<string> {
  const config = getConfig();
  const targetDevice = getDeviceParam(config, params.device, params.locationId);
  const deviceManager = getDeviceManager();
  const device = await deviceManager.getDevice(targetDevice);

  const swingMap: Record<string, string> = {
    off: '0',
    vertical: '1',
    horizontal: '2',
    '3d': '3',
  };

  await device.set({ f_dir: swingMap[params.mode] });

  return `${getDisplayName(targetDevice)} swing mode set to ${params.mode.toUpperCase()}.`;
}

export const daikinPowerfulTool: SkillTool = {
  name: 'daikin_powerful',
  description: 'Toggle powerful mode (maximum cooling/heating) on a Daikin air conditioner.',
  parameters: {
    type: 'object',
    properties: {
      device: {
        type: 'string',
        description: 'Name of the device',
      },
      locationId: {
        type: 'string',
        description: 'Location ID if device name exists in multiple locations',
      },
      enabled: {
        type: 'string',
        enum: ['on', 'off'],
        description: 'Enable or disable powerful mode',
      },
    },
    required: ['enabled'],
  },
};

export async function daikinPowerful(params: { device?: string; locationId?: string; enabled: 'on' | 'off' }): Promise<string> {
  const config = getConfig();
  const targetDevice = getDeviceParam(config, params.device, params.locationId);
  const deviceManager = getDeviceManager();
  const device = await deviceManager.getDevice(targetDevice);

  await device.setAdvancedMode('powerful', params.enabled);

  return `${getDisplayName(targetDevice)} powerful mode ${params.enabled.toUpperCase()}.`;
}

export const daikinEconoTool: SkillTool = {
  name: 'daikin_econo',
  description: 'Toggle econo mode (energy-efficient) on a Daikin air conditioner.',
  parameters: {
    type: 'object',
    properties: {
      device: {
        type: 'string',
        description: 'Name of the device',
      },
      locationId: {
        type: 'string',
        description: 'Location ID if device name exists in multiple locations',
      },
      enabled: {
        type: 'string',
        enum: ['on', 'off'],
        description: 'Enable or disable econo mode',
      },
    },
    required: ['enabled'],
  },
};

export async function daikinEcono(params: { device?: string; locationId?: string; enabled: 'on' | 'off' }): Promise<string> {
  const config = getConfig();
  const targetDevice = getDeviceParam(config, params.device, params.locationId);
  const deviceManager = getDeviceManager();
  const device = await deviceManager.getDevice(targetDevice);

  await device.setAdvancedMode('econo', params.enabled);

  return `${getDisplayName(targetDevice)} econo mode ${params.enabled.toUpperCase()}.`;
}

export const daikinStreamerTool: SkillTool = {
  name: 'daikin_streamer',
  description: 'Toggle streamer air purifier on a Daikin air conditioner.',
  parameters: {
    type: 'object',
    properties: {
      device: {
        type: 'string',
        description: 'Name of the device',
      },
      locationId: {
        type: 'string',
        description: 'Location ID if device name exists in multiple locations',
      },
      enabled: {
        type: 'string',
        enum: ['on', 'off'],
        description: 'Enable or disable streamer',
      },
    },
    required: ['enabled'],
  },
};

export async function daikinStreamer(params: { device?: string; locationId?: string; enabled: 'on' | 'off' }): Promise<string> {
  const config = getConfig();
  const targetDevice = getDeviceParam(config, params.device, params.locationId);
  const deviceManager = getDeviceManager();
  const device = await deviceManager.getDevice(targetDevice);

  await device.setStreamer(params.enabled);

  return `${getDisplayName(targetDevice)} streamer ${params.enabled.toUpperCase()}.`;
}

export const daikinHolidayTool: SkillTool = {
  name: 'daikin_holiday',
  description: 'Toggle holiday/away mode on a Daikin air conditioner.',
  parameters: {
    type: 'object',
    properties: {
      device: {
        type: 'string',
        description: 'Name of the device',
      },
      locationId: {
        type: 'string',
        description: 'Location ID if device name exists in multiple locations',
      },
      enabled: {
        type: 'string',
        enum: ['on', 'off'],
        description: 'Enable or disable holiday mode',
      },
    },
    required: ['enabled'],
  },
};

export async function daikinHoliday(params: { device?: string; locationId?: string; enabled: 'on' | 'off' }): Promise<string> {
  const config = getConfig();
  const targetDevice = getDeviceParam(config, params.device, params.locationId);
  const deviceManager = getDeviceManager();
  const device = await deviceManager.getDevice(targetDevice);

  await device.setHoliday(params.enabled);

  return `${getDisplayName(targetDevice)} holiday mode ${params.enabled.toUpperCase()}.`;
}
