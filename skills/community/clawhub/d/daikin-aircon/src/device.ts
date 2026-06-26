import { DaikinFactory, Appliance } from 'daikin-ts';
import type { DaikinDeviceConfig } from './config.js';

export class DeviceManager {
  private instances: Map<string, Appliance> = new Map();

  async getDevice(config: DaikinDeviceConfig): Promise<Appliance> {
    const cacheKey = config.id || config.ip;

    if (this.instances.has(cacheKey)) {
      return this.instances.get(cacheKey)!;
    }

    const options: { key?: string; password?: string } = {};
    if (config.key) options.key = config.key;
    if (config.password) options.password = config.password;

    const device = await DaikinFactory(config.ip, {
      deviceId: config.ip,
      ...options,
    });

    this.instances.set(cacheKey, device);
    return device;
  }

  async getDeviceStatus(config: DaikinDeviceConfig): Promise<Appliance> {
    const device = await this.getDevice(config);
    await device.updateStatus();
    return device;
  }

  clearCache(deviceId?: string): void {
    if (deviceId) {
      this.instances.delete(deviceId);
    } else {
      this.instances.clear();
    }
  }
}

let deviceManagerInstance: DeviceManager | null = null;

export function getDeviceManager(): DeviceManager {
  if (!deviceManagerInstance) {
    deviceManagerInstance = new DeviceManager();
  }
  return deviceManagerInstance;
}
