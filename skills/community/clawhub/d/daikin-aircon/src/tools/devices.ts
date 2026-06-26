import type { SkillTool } from '../types.js';
import { getConfig, type DaikinDeviceConfig, DeviceNotFoundError } from '../config.js';
import { getDeviceManager } from '../device.js';

export const daikinListTool: SkillTool = {
  name: 'daikin_list',
  description: 'List all configured Daikin air conditioner devices with their names, IP addresses, and connection status.',
  parameters: {
    type: 'object',
    properties: {},
  },
};

export async function daikinList(): Promise<string> {
  const config = getConfig();
  const devices = config.getDevices();

  if (devices.length === 0) {
    return 'No devices configured. Use daikin_discover to find devices or daikin_add to add one manually.';
  }

  const defaultDevice = config.getDefaultDeviceName();
  let result = `Configured devices (${devices.length}):\n\n`;

  for (const device of devices) {
    const isDefault = device.id === defaultDevice;
    const displayName = device.name || device.id;
    const location = device.locationName || device.locationId;
    
    result += `${isDefault ? '★ ' : '- '}${displayName}`;
    if (location) {
      result += ` (${location})`;
    }
    result += '\n';
    result += `  IP: ${device.ip}\n`;
    result += `  Type: ${device.type || 'auto-detect'}\n`;
    if (device.key) result += `  API Key: configured\n`;
    if (device.password) result += `  Password: configured\n`;
    if (device.enabled === false) result += `  Status: disabled\n`;
    result += '\n';
  }

  return result;
}

export const daikinAddTool: SkillTool = {
  name: 'daikin_add',
  description: 'Add a new Daikin air conditioner device to the configuration.',
  parameters: {
    type: 'object',
    properties: {
      name: {
        type: 'string',
        description: 'User-friendly name for the device (e.g., living-room, bedroom)',
      },
      ip: {
        type: 'string',
        description: 'IP address of the Daikin device',
      },
      locationId: {
        type: 'string',
        description: 'Optional location ID (e.g., home, beach-house) if multiple locations',
      },
      locationName: {
        type: 'string',
        description: 'Optional location display name (e.g., Family Home, Beach House)',
      },
      type: {
        type: 'string',
        enum: ['brp069', 'brp072c', 'brp084', 'airbase', 'skyfi'],
        description: 'Device type (optional, will auto-detect if not specified)',
      },
      key: {
        type: 'string',
        description: 'API key for BRP072C devices (required for HTTPS adapter)',
      },
      password: {
        type: 'string',
        description: 'Password for SkyFi devices',
      },
    },
    required: ['name', 'ip'],
  },
};

export async function daikinAdd(params: {
  name: string;
  ip: string;
  locationId?: string;
  locationName?: string;
  type?: 'brp069' | 'brp072c' | 'brp084' | 'airbase' | 'skyfi';
  key?: string;
  password?: string;
}): Promise<string> {
  const config = getConfig();

  const id = params.name.toLowerCase().replace(/\s+/g, '-');
  
  const existing = config.getDevice(params.name, params.locationId);
  if (existing) {
    const loc = params.locationId ? ` at ${params.locationId}` : '';
    return `Device "${params.name}"${loc} already exists at IP ${existing.ip}. Use daikin_remove first to remove it.`;
  }

  const deviceConfig: DaikinDeviceConfig = {
    id,
    name: params.name,
    ip: params.ip,
    locationId: params.locationId,
    locationName: params.locationName,
    type: params.type,
    key: params.key,
    password: params.password,
    enabled: true,
  };

  try {
    config.addDevice(deviceConfig);
  } catch (error) {
    if (error instanceof Error && error.message.includes('already exists')) {
      return error.message;
    }
    throw error;
  }

  let result = `Device "${params.name}" added successfully at ${params.ip}`;
  if (params.locationName) {
    result += ` (${params.locationName})`;
  }
  if (params.type) {
    result += ` (type: ${params.type})`;
  }
  result += '\n\nYou can now control this device using its name.';

  return result;
}

export const daikinRemoveTool: SkillTool = {
  name: 'daikin_remove',
  description: 'Remove a configured Daikin air conditioner device.',
  parameters: {
    type: 'object',
    properties: {
      name: {
        type: 'string',
        description: 'Name or ID of the device to remove',
      },
      locationId: {
        type: 'string',
        description: 'Location ID if device name exists in multiple locations',
      },
    },
    required: ['name'],
  },
};

export async function daikinRemove(params: { name: string; locationId?: string }): Promise<string> {
  const config = getConfig();
  const deviceManager = getDeviceManager();

  const device = config.getDevice(params.name, params.locationId);
  if (!device) {
    const matching = config.findDevicesByName(params.name);
    if (matching.length > 1) {
      const locations = matching.map(d => 
        d.locationName || d.locationId || 'default'
      ).join(', ');
      return `Multiple devices found with name "${params.name}". Please specify location: ${locations}`;
    }
    return `Device "${params.name}" not found. Use daikin_list to see available devices.`;
  }

  deviceManager.clearCache(device.id);
  
  const displayName = device.name || device.id;
  const location = device.locationName || device.locationId;
  config.removeDevice(params.name, params.locationId);

  let result = `Device "${displayName}" has been removed.`;
  if (location) {
    result += ` (${location})`;
  }
  return result;
}

export const daikinSetDefaultTool: SkillTool = {
  name: 'daikin_set_default',
  description: 'Set the default device to use when no device name is specified.',
  parameters: {
    type: 'object',
    properties: {
      name: {
        type: 'string',
        description: 'Name or ID of the device to set as default',
      },
      locationId: {
        type: 'string',
        description: 'Location ID if device name exists in multiple locations',
      },
    },
    required: ['name'],
  },
};

export async function daikinSetDefault(params: { name: string; locationId?: string }): Promise<string> {
  const config = getConfig();

  const device = config.getDevice(params.name, params.locationId);
  if (!device) {
    return `Device "${params.name}" not found. Use daikin_list to see available devices.`;
  }

  config.setDefaultDevice(params.name, params.locationId);
  
  const displayName = device.name || device.id;
  return `Default device set to "${displayName}". Commands without a device name will now use this device.`;
}

export const daikinUpdateTool: SkillTool = {
  name: 'daikin_update',
  description: 'Update device settings (IP, type, key, password, location).',
  parameters: {
    type: 'object',
    properties: {
      name: {
        type: 'string',
        description: 'Name or ID of the device to update',
      },
      locationId: {
        type: 'string',
        description: 'Location ID if device name exists in multiple locations',
      },
      newIp: {
        type: 'string',
        description: 'New IP address',
      },
      newName: {
        type: 'string',
        description: 'New device name',
      },
      type: {
        type: 'string',
        enum: ['brp069', 'brp072c', 'brp084', 'airbase', 'skyfi'],
        description: 'Device type',
      },
      key: {
        type: 'string',
        description: 'API key for BRP072C devices',
      },
      password: {
        type: 'string',
        description: 'Password for SkyFi devices',
      },
    },
    required: ['name'],
  },
};

export async function daikinUpdate(params: {
  name: string;
  locationId?: string;
  newIp?: string;
  newName?: string;
  type?: 'brp069' | 'brp072c' | 'brp084' | 'airbase' | 'skyfi';
  key?: string;
  password?: string;
}): Promise<string> {
  const config = getConfig();
  const deviceManager = getDeviceManager();

  const device = config.getDevice(params.name, params.locationId);
  if (!device) {
    return `Device "${params.name}" not found. Use daikin_list to see available devices.`;
  }

  const updates: Partial<DaikinDeviceConfig> = {};
  
  if (params.newIp) updates.ip = params.newIp;
  if (params.newName) {
    updates.name = params.newName;
    updates.id = params.newName.toLowerCase().replace(/\s+/g, '-');
  }
  if (params.type) updates.type = params.type;
  if (params.key) updates.key = params.key;
  if (params.password) updates.password = params.password;

  deviceManager.clearCache(device.id);
  
  try {
    config.updateDevice(device.id, device.locationId, updates);
  } catch (error) {
    if (error instanceof DeviceNotFoundError) {
      return error.message;
    }
    throw error;
  }

  const displayName = (updates.name || device.name || device.id);
  return `Device "${displayName}" updated successfully.`;
}
