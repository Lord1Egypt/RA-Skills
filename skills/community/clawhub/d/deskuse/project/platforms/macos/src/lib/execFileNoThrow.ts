import { execFile } from 'node:child_process'

export function execFileNoThrow(
  file: string,
  args: string[],
  options: { input?: string; useCwd?: boolean } = {},
): Promise<{ code: number; stdout: string; stderr: string }> {
  return new Promise(resolve => {
    const child = execFile(
      file,
      args,
      {
        cwd: options.useCwd === false ? undefined : process.cwd(),
        encoding: 'utf8',
        maxBuffer: 32 * 1024 * 1024,
      },
      (error, stdout, stderr) => {
        const code = typeof (error as NodeJS.ErrnoException | null)?.code === 'number'
          ? (error as NodeJS.ErrnoException).code as unknown as number
          : error
            ? 1
            : 0
        resolve({ code, stdout: stdout ?? '', stderr: stderr ?? '' })
      },
    )

    if (options.input !== undefined) {
      child.stdin?.end(options.input)
    }
  })
}
