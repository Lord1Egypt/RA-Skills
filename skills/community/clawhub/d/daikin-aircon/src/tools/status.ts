import type { SkillTool } from '../types.js';
import { getConfig } from '../config.js';
import { getDeviceManager } from '../device.js';

export const daikinStatusTool: SkillTool = {
  name: 'daikin_status',
  description: 'Get the current status of a Daikin air conditioner including power, mode, temperature, fan speed, and other information.',
  parameters: {
    type: 'object',
    properties: {
      device: {
        type: 'string',
        description: 'Name of the device (optional if only one device is configured)',
      },
      locationId: {
        type: 'string',
        description: 'Location ID if device name exists in multiple locations',
      },
    },
  },
};

export async function daikinStatus(params: { device?: string; locationId?: string }): Promise<string> {
  const config = getConfig();

  let targetDevice;
  if (params.device) {
    targetDevice = config.getDevice(params.device, params.locationId);
    if (!targetDevice) {
      const matches = config.findDevicesByName(params.device);
      if (matches.length > 1) {
        const locations = matches.map(d => 
          d.locationName || d.locationId || 'default'
        ).join(', ');
        return `Multiple devices found with name "${params.device}". Please specify location: ${locations}`;
      }
      return `Device "${params.device}" not found. Use daikin_list to see available devices.`;
    }
  } else {
    targetDevice = config.getDefaultDevice();
    if (!targetDevice) {
      return 'No device specified and no default device set. Use daikin_list to see available devices or specify a device name.';
    }
  }

  const deviceManager = getDeviceManager();
  const device = await deviceManager.getDeviceStatus(targetDevice);

  const values = device.values;
  const power = values.get('pow') === '1' ? 'ON' : 'OFF';
  const mode = Appliance.daikinToHuman('mode', values.get('mode') || '') || values.get('mode') || 'unknown';
  const insideTemp = device.insideTemperature;
  const targetTemp = device.targetTemperature;
  const outsideTemp = device.outsideTemperature;
  const fanRate = Appliance.daikinToHuman('f_rate', values.get('f_rate') || '') || values.get('f_rate') || 'unknown';
  const fanDir = Appliance.daikinToHuman('f_dir', values.get('f_dir') || '') || values.get('f_dir') || 'unknown';
  const adv = values.get('adv') || '';

  const displayName = targetDevice.name || targetDevice.id;
  const location = targetDevice.locationName || targetDevice.locationId;

  let result = `Status for ${displayName}`;
  if (location) {
    result += ` (${location})`;
  }
  result += ':\n\n';
  
  result += `Power: ${power}\n`;
  result += `Mode: ${mode}\n`;
  result += `Target Temperature: ${targetTemp !== null ? targetTemp + '°C' : 'N/A'}\n`;
  result += `Inside Temperature: ${insideTemp !== null ? insideTemp + '°C' : 'N/A'}\n`;
  result += `Outside Temperature: ${outsideTemp !== null ? outsideTemp + '°C' : 'N/A'}\n`;
  result += `Fan Rate: ${fanRate}\n`;
  result += `Fan Direction: ${fanDir}\n`;

  if (device.humidity !== null) {
    result += `Humidity: ${device.humidity}%\n`;
  }

  if (device.compressorFrequency !== null) {
    result += `Compressor Frequency: ${device.compressorFrequency} Hz\n`;
  }

  if (adv) {
    const advMode = Appliance.daikinToHuman('adv', adv);
    result += `Advanced Mode: ${advMode || adv}\n`;
  }

  if (device.supportFilterDirty && device.filterDirty !== null) {
    result += `Filter Status: ${device.filterDirty === 1 ? 'Needs cleaning' : 'OK'}\n`;
  }

  return result;
}

const Appliance = (await import('daikin-ts')).Appliance;
