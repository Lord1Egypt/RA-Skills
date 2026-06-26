import * as fs from 'fs';
import * as path from 'path';
import { fileURLToPath } from 'url';

export interface DaikinDeviceConfig {
  id: string;
  name?: string;
  locationId?: string;
  locationName?: string;
  ip: string;
  type?: 'brp069' | 'brp072c' | 'brp084' | 'airbase' | 'skyfi';
  key?: string;
  password?: string;
  enabled?: boolean;
  lastSeen?: string;
}

export interface ConfigData {
  devices: DaikinDeviceConfig[];
  defaultDevice?: string;
}

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export class DeviceConfig {
  private configPath: string;
  private data: ConfigData;

  constructor(configPath?: string) {
    if (configPath) {
      this.configPath = configPath;
    } else {
      const skillDir = path.resolve(__dirname, '..');
      this.configPath = path.join(skillDir, 'data', 'devices.json');
    }

    this.data = this.load();
  }

  private load(): ConfigData {
    try {
      if (fs.existsSync(this.configPath)) {
        const content = fs.readFileSync(this.configPath, 'utf-8');
        return JSON.parse(content);
      }
    } catch (error) {
      console.error('Error loading config:', error);
    }
    return { devices: [] };
  }

  private save(): void {
    const dir = path.dirname(this.configPath);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
    fs.writeFileSync(this.configPath, JSON.stringify(this.data, null, 2), 'utf-8');
  }

  private getUniqueKey(device: DaikinDeviceConfig): string {
    const loc = device.locationId || 'default';
    return `${loc}:${device.id}`;
  }

  getDevices(): DaikinDeviceConfig[] {
    return this.data.devices;
  }

  getDevice(name: string, locationId?: string): DaikinDeviceConfig | undefined {
    const normalizedName = name.toLowerCase().replace(/\s+/g, '-');
    
    let matches = this.data.devices.filter(d => {
      const matchId = d.id.toLowerCase() === normalizedName;
      const matchName = (d.name || d.id).toLowerCase().replace(/\s+/g, '-') === normalizedName;
      return matchId || matchName;
    });

    if (locationId) {
      matches = matches.filter(d => (d.locationId || 'default') === locationId);
    }

    if (matches.length === 1) {
      return matches[0];
    }
    
    if (matches.length > 1 && !locationId) {
      return undefined;
    }
    
    return undefined;
  }

  getDeviceById(id: string, locationId?: string): DaikinDeviceConfig | undefined {
    return this.data.devices.find(d => {
      const locMatch = locationId ? (d.locationId || 'default') === locationId : true;
      return d.id === id && locMatch;
    });
  }

  getDefaultDevice(): DaikinDeviceConfig | undefined {
    if (this.data.defaultDevice) {
      return this.getDevice(this.data.defaultDevice);
    }
    return this.data.devices[0];
  }

  addDevice(device: DaikinDeviceConfig): void {
    const key = this.getUniqueKey(device);
    const existing = this.data.devices.find(d => this.getUniqueKey(d) === key);
    if (existing) {
      throw new Error(`Device "${device.id}" already exists at this location`);
    }
    this.data.devices.push(device);
    this.save();
  }

  updateDevice(id: string, locationId: string | undefined, updates: Partial<DaikinDeviceConfig>): void {
    const device = this.getDeviceById(id, locationId);
    if (!device) {
      throw new DeviceNotFoundError(id, locationId);
    }
    Object.assign(device, updates);
    this.save();
  }

  removeDevice(name: string, locationId?: string): void {
    const device = this.getDevice(name, locationId);
    if (!device) {
      throw new DeviceNotFoundError(name, locationId);
    }
    
    const key = this.getUniqueKey(device);
    const index = this.data.devices.findIndex(d => this.getUniqueKey(d) === key);
    if (index === -1) {
      throw new DeviceNotFoundError(name, locationId);
    }
    this.data.devices.splice(index, 1);
    this.save();
  }

  setDefaultDevice(name: string, locationId?: string): void {
    const device = this.getDevice(name, locationId);
    if (!device) {
      throw new DeviceNotFoundError(name, locationId);
    }
    this.data.defaultDevice = device.id;
    this.save();
  }

  getDefaultDeviceName(): string | undefined {
    return this.data.defaultDevice;
  }

  findDevicesByName(name: string): DaikinDeviceConfig[] {
    const normalizedName = name.toLowerCase().replace(/\s+/g, '-');
    
    return this.data.devices.filter(d => {
      const matchId = d.id.toLowerCase() === normalizedName;
      const matchName = (d.name || d.id).toLowerCase().replace(/\s+/g, '-') === normalizedName;
      return matchId || matchName;
    });
  }
}

export class DeviceNotFoundError extends Error {
  constructor(name: string, locationId?: string) {
    const loc = locationId ? ` at ${locationId}` : '';
    super(`Device "${name}"${loc} not found`);
    this.name = 'DeviceNotFoundError';
  }
}

let configInstance: DeviceConfig | null = null;

export function getConfig(configPath?: string): DeviceConfig {
  if (!configInstance) {
    configInstance = new DeviceConfig(configPath);
  }
  return configInstance;
}

export function resetConfig(): void {
  configInstance = null;
}
