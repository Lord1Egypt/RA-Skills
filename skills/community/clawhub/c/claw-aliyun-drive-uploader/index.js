/**
 * 阿里云盘技能 - Node.js 入口
 * 实际调用 Python SDK 执行操作
 */
import { readFileSync, existsSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const PYTHON_SCRIPT = resolve(__dirname, 'scripts/api.py');

// 尝试多个可能的 Python venv 路径
const PYTHON_PATHS = [
  '/tmp/venv/bin/python3',
  '/usr/bin/python3',
  'python3'
];

/**
 * 从 .env 读取 token
 */
function getEnvToken() {
  const envPath = resolve(process.cwd(), '.env');
  if (!existsSync(envPath)) return null;
  const content = readFileSync(envPath, 'utf8');
  const match = content.match(/ALIYUN_DRIVE_REFRESH_TOKEN="([^"]+)"/);
  return match ? match[1] : null;
}

/**
 * 查找可用的 Python
 */
function findPython() {
  for (const p of PYTHON_PATHS) {
    try {
      const { execSync } = require('child_process');
      execSync(`${p} --version`, { encoding: 'utf8', timeout: 5000 });
      return p;
    } catch {
      // try next
    }
  }
  return 'python3';
}

/**
 * 执行 Python 脚本
 */
async function execPython(args) {
  const token = getEnvToken();
  if (!token) throw new Error('ALIYUN_DRIVE_REFRESH_TOKEN not found in .env');

  const envPath = resolve(process.cwd(), '.env');
  const python = findPython();
  const cmd = [python, PYTHON_SCRIPT, ...args, '--token', token, '--save-token', envPath];

  const { execSync } = require('child_process');
  const output = execSync(cmd.join(' '), { encoding: 'utf8', timeout: 120000, stdio: ['pipe', 'pipe', 'pipe'] });
  return JSON.parse(output.trim());
}

export default async function run(input) {
  const { action } = input;

  if (!action) {
    return { success: false, message: 'action is required' };
  }

  try {
    switch (action) {
      case 'upload': {
        const { file_path, target_folder, parent_id } = input;
        if (!file_path) return { success: false, message: 'file_path required' };

        const args = ['upload', '--file-path', file_path];
        if (target_folder) args.push('--target-folder', target_folder);
        if (parent_id) args.push('--parent-id', parent_id);

        return await execPython(args);
      }

      case 'list': {
        const { parent_id } = input;
        const args = ['list'];
        if (parent_id) args.push('--parent-id', parent_id);
        return await execPython(args);
      }

      case 'create_folder': {
        const { name, parent_id } = input;
        if (!name) return { success: false, message: 'name required' };
        const args = ['create_folder', '--name', name];
        if (parent_id) args.push('--parent-id', parent_id);
        return await execPython(args);
      }

      case 'search': {
        const { name, parent_id } = input;
        if (!name) return { success: false, message: 'name required' };
        const args = ['search', '--name', name];
        if (parent_id) args.push('--parent-id', parent_id);
        return await execPython(args);
      }

      case 'share': {
        const { file_id } = input;
        if (!file_id) return { success: false, message: 'file_id required' };
        return await execPython(['share', '--file-id', file_id]);
      }

      case 'delete': {
        const { file_id } = input;
        if (!file_id) return { success: false, message: 'file_id required' };
        return await execPython(['delete', '--file-id', file_id]);
      }

      case 'download_url': {
        const { file_id } = input;
        if (!file_id) return { success: false, message: 'file_id required' };
        return await execPython(['download_url', '--file-id', file_id]);
      }

      case 'user_info':
        return await execPython(['user_info']);

      default:
        return { success: false, message: `Unknown action: ${action}` };
    }
  } catch (e) {
    return { success: false, message: e.message };
  }
}
