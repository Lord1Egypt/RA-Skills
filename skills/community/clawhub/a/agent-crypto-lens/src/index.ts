// src/index.ts
import * as dotenv from 'dotenv';
dotenv.config();

// 간단한 Mock ACP Agent (SDK 설치 없이 테스트)
class MockAcpAgent {
  onJob(callback: (job: any) => Promise<void>) {
    console.log('[Mock] ACP Job 수신 대기 중...');
    // 3초 후 테스트 Job 발송 시뮬레이션
    setTimeout(async () => {
      const mockJob = {
        id: 'job-crypto-123',
        payload: {
          token: 'Bitcoin', // 실제 CoinGecko 심볼은 'bitcoin'
          analysis_type: 'full'
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
