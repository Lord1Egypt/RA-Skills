import * as dgram from 'dgram';
import * as os from 'os';
import { parseResponse } from 'daikin-ts';
import type { DiscoveryDevice } from 'daikin-ts';

const UDP_SRC_PORT = 30000;
const UDP_DST_PORT = 30050;
const GRACE_SECONDS = 2;
const DISCOVERY_MSG = 'DAIKIN_UDP/common/basic_info';

interface NetworkInterfaceInfoIPv4 extends os.NetworkInterfaceInfoIPv4 {
  broadcast?: string;
}

export interface DiscoveredDevice {
  name: string;
  ip: string;
  mac: string;
  port?: number;
}

export class DaikinDiscovery {
  private socket: dgram.Socket;
  private devices: Map<string, DiscoveredDevice> = new Map();

  constructor() {
    this.socket = dgram.createSocket({ type: 'udp4', reuseAddr: true });
  }

  async poll(targetIp?: string): Promise<DiscoveredDevice[]> {
    return new Promise((resolve, reject) => {
      const broadcastIps = this.getBroadcastIps(targetIp);

      const timeout = setTimeout(() => {
        this.socket.close();
        resolve(Array.from(this.devices.values()));
      }, GRACE_SECONDS * 1000);

      this.socket.on('message', (msg, rinfo) => {
        try {
          const data = parseResponse(msg.toString('utf-8'));

          if (!data.mac) {
            throw new Error('No MAC found for device');
          }

          const device: DiscoveredDevice = {
            name: data.name || '',
            ip: rinfo.address,
            mac: data.mac,
            port: rinfo.port,
          };

          this.devices.set(data.mac, device);
        } catch {
          // Invalid message, ignore
        }
      });

      this.socket.on('error', (err) => {
        clearTimeout(timeout);
        this.socket.close();
        reject(err);
      });

      this.socket.bind(UDP_SRC_PORT, () => {
        this.socket.setBroadcast(true);

        for (const ip of broadcastIps) {
          const message = Buffer.from(DISCOVERY_MSG, 'utf-8');
          this.socket.send(message, 0, message.length, UDP_DST_PORT, ip, (err) => {
            if (err) {
              console.error('Error sending discovery:', err);
            }
          });
        }
      });
    });
  }

  private getBroadcastIps(targetIp?: string): string[] {
    if (targetIp) {
      return [targetIp];
    }

    const interfaces = os.networkInterfaces();
    const broadcastIps: string[] = [];

    for (const name in interfaces) {
      const iface = interfaces[name];
      if (!iface) continue;

      for (const info of iface) {
        const ipv4Info = info as NetworkInterfaceInfoIPv4;
        if (ipv4Info.family === 'IPv4' && ipv4Info.broadcast) {
          broadcastIps.push(ipv4Info.broadcast);
        }
      }
    }

    return broadcastIps;
  }
}

export async function discoverDevices(targetIp?: string): Promise<DiscoveredDevice[]> {
  const discovery = new DaikinDiscovery();
  return discovery.poll(targetIp);
}
