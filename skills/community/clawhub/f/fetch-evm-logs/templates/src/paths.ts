import fs from 'fs';
import path from 'path';

export const OUTPUT_DIR = path.resolve(process.cwd(), 'output');
export const ABI_DIR = path.resolve(process.cwd(), 'src/abi');

export function abiFileBaseName(address: string, chainId: number) {
  return `abi_${address.toLowerCase()}_${chainId}`;
}

export function abiJsonPath(address: string, chainId: number) {
  return path.join(ABI_DIR, `${abiFileBaseName(address, chainId)}.json`);
}

export function contractDirName(address: string, chainId: number) {
  return `${address.toLowerCase()}_${chainId}`;
}

export function contractOutputDir(address: string, chainId: number) {
  return path.join(OUTPUT_DIR, contractDirName(address, chainId));
}

export function ensureContractOutputDir(address: string, chainId: number) {
  fs.mkdirSync(contractOutputDir(address, chainId), { recursive: true });
}

export function logsTxtPath(address: string, chainId: number) {
  return path.join(contractOutputDir(address, chainId), 'logs.txt');
}

export function logsJsonPath(address: string, chainId: number) {
  return path.join(contractOutputDir(address, chainId), 'logs.json');
}
