import os from 'os';
import path from 'path';

export function stateDir() {
  return process.env.MATRIX_STATE_DIR
    || process.env.GEWEI_STATE_DIR
    || path.join(os.homedir(), '.gewei-skills');
}
