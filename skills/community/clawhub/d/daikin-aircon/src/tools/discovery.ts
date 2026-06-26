import type { SkillTool } from '../types.js';
import { discoverDevices, type DiscoveredDevice } from '../discovery.js';

export const daikinDiscoverTool: SkillTool = {
  name: 'daikin_discover',
  description: 'Discover Daikin air conditioner devices on the local network using UDP broadcast. Returns a list of found devices with their IP addresses, MAC addresses, and names.',
  parameters: {
    type: 'object',
    properties: {
      targetIp: {
        type: 'string',
        description: 'Optional specific IP or subnet to scan (e.g., 192.168.1.255)',
      },
    },
  },
};

export async function daikinDiscover(params: { targetIp?: string }): Promise<string> {
  const devices = await discoverDevices(params.targetIp);

  if (devices.length === 0) {
    return 'No Daikin devices found on the network. Try checking the IP address manually or ensure devices are powered on and connected to the same network.';
  }

  let result = `Found ${devices.length} Daikin device(s):\n\n`;
  
  for (const device of devices) {
    result += `- IP: ${device.ip}\n`;
    result += `  MAC: ${device.mac}\n`;
    result += `  Name: ${device.name || '(none)'}\n\n`;
  }

  result += 'To add a device, use daikin_add with the device name and IP address.';

  return result;
}
