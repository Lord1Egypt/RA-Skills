// src/index.ts
import * as dotenv from 'dotenv';
import * as path from 'path';

// .env 파일 명시적 로드
dotenv.config({ path: path.resolve(__dirname, '../.env') });

console.log('[Debug] ANTHROPIC_API_KEY Loaded:', process.env.ANTHROPIC_API_KEY ? 'Yes' : 'No');
console.log('[Debug] TAVILY_API_KEY Loaded:', process.env.TAVILY_API_KEY ? 'Yes' : 'No');

// 간단한 Mock ACP Agent (SDK 설치 없이 테스트)
class MockAcpAgent {
  onJob(callback: (job: any) => Promise<void>) {
    console.log('[Mock] ACP Job 수신 대기 중...');
    // 3초 후 테스트 Job 발송 시뮬레이션
    setTimeout(async () => {
      const mockJob = {
        id: 'job-test-123',
        payload: {
          topic: 'Bitcoin',
          period: '1d',
          max_items: 3
        },
        complete: (res: any) => console.log('[Mock] Job 완료:', JSON.stringify(res, null, 2)),
        reject: (err: any) => console.error('[Mock] Job 실패:', err)
      };
      await callback(mockJob);
    }, 3000);
  }
  start() {
    console.log('[Mock] 에이전트 시작됨.');
  }
}

import { handleJob } from './handler';

const agent = new MockAcpAgent();

agent.onJob(async (job: any) => {
  console.log(`[수신] Job ID: ${job.id}`);
  try {
    const result = await handleJob(job.payload);
    await job.complete(result);
  } catch (error: any) {
    console.error(`[오류] ${error.message}`);
    await job.reject(error.message);
  }
});

agent.start();
