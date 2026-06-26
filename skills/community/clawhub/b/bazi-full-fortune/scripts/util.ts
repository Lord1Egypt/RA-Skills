export interface ParseArgsResult {
  time: string;
  gender: 0 | 1;
  sect: 1 | 2;
}

export function parseArgs(args: string[]): ParseArgsResult {
  const [, , time, genderString, sectString] = args;

  let gender: 0 | 1 = 1;
  if (genderString) {
    gender = Number.parseInt(genderString) as 0 | 1;
    if (isNaN(gender) || ![0, 1].includes(gender)) {
      throw new Error(`性别参数无效。男性传 1，女性传 0。`);
    }
  }

  let sect: 1 | 2 = 2;
  if (sectString) {
    sect = Number.parseInt(sectString) as 1 | 2;
    if (isNaN(sect) || ![1, 2].includes(sect)) {
      throw new Error(
        `早晚子时配置参数无效。传 1 表示 23:00-23:59 日干支为明天，传 2 表示 23:00-23:59 日干支为当天。`
      );
    }
  }

  return { time, gender, sect };
}
