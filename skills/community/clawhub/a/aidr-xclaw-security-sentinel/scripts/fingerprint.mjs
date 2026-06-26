#!/usr/bin/env node
import { createHash } from 'crypto';
import { execSync } from 'child_process';
import { platform } from 'os';

function getRawMachineId() {
  const commands = {
    darwin:  'ioreg -rd1 -c IOPlatformExpertDevice',
    win32:   'reg query "HKLM\\SOFTWARE\\Microsoft\\Cryptography" /v MachineGuid',
    linux:   '(cat /var/lib/dbus/machine-id /etc/machine-id 2>/dev/null || hostname) | head -n 1',
    freebsd: 'kenv -q smbios.system.uuid || sysctl -n kern.hostuuid'
  };
  const cmd = commands[platform()];
  if (!cmd) throw new Error(`Unsupported platform: ${platform()}`);
  const output = execSync(cmd, { encoding: 'utf8' });

  if (platform() === 'darwin') {
    return output.split('IOPlatformUUID')[1].split('\n')[0]
      .replace(/[=\s"]/gi, '').toLowerCase();
  }
  return output.trim().toLowerCase();
}

const rawId = getRawMachineId();
const fingerprint = createHash('sha256').update(rawId).digest('hex');
console.log(fingerprint);
