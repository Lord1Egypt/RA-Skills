import {
  closeSync, constants, fchmodSync, fstatSync, ftruncateSync, openSync, writeFileSync,
} from 'node:fs';

export function writePrivateFile(file, content) {
  // Open without truncating so permission checks happen before changing the file.
  const fd = openSync(file, constants.O_WRONLY | constants.O_CREAT | constants.O_NONBLOCK, 0o600);
  try {
    if (!fstatSync(fd).isFile()) throw new Error('Amber can only write private data to a regular file.');
    fchmodSync(fd, 0o600);
    ftruncateSync(fd, 0);
    writeFileSync(fd, content, 'utf8');
  } finally {
    closeSync(fd);
  }
}
