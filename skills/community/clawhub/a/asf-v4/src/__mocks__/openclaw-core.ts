/**
 * OpenClaw Core Mock
 */

export const video_generate = jest.fn().mockResolvedValue({
  status: 'success',
  videoPath: '/videos/mock-output.mp4',
  durationMs: 5000,
  costEstimate: 0.05,
  qualityScore: 0.85,
  metadata: {
    model: 'wan2.6-t2v',
    resolution: '1080P',
    duration: 5,
    aspectRatio: '16:9',
  },
});
