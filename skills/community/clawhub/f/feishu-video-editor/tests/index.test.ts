/**
 * 单元测试
 */

import { main } from '../src/index';

describe('feishu-video-editor', () => {
  test('should show help when command is help', async () => {
    const result = await main('help', []);
    expect(result.message).toContain('AI 视频剪辑 Skill');
  });

  test('should require video path for trim_silence', async () => {
    const result = await main('trim_silence', []);
    expect(result.message).toContain('请提供视频');
  });

  test('should require time args for crop', async () => {
    const result = await main('crop', ['video.mp4']);
    expect(result.message).toContain('起止时间');
  });
});
