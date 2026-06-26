# API 연동 가이드

현재 스크립트는 mock 데이터를 반환합니다. 실제 API를 연동하려면 각 함수의 TODO 섹션을 구현하세요.

## 1. 네이버 스마트스토어 API

### API 키 발급

1. [네이버 개발자 센터](https://developers.naver.com/) 로그인
2. 애플리케이션 등록
3. Client ID, Client Secret 발급
4. 스마트스토어 API 사용 신청

### 구현 (scripts/collect.js)

```javascript
// collectNaver 함수 수정
async function collectNaver(config, date) {
  if (!config.sources.naver.enabled) {
    return null;
  }
  
  console.log('📦 네이버 스마트스토어 데이터 수집 중...');
  
  const clientId = config.sources.naver.clientId;
  const clientSecret = config.sources.naver.clientSecret;
  
  // 날짜 범위 설정 (해당 날짜 00:00 ~ 23:59)
  const startDate = new Date(date);
  startDate.setHours(0, 0, 0, 0);
  const endDate = new Date(date);
  endDate.setHours(23, 59, 59, 999);
  
  // API 호출 (예시)
  const axios = require('axios');
  
  const response = await axios.get('https://api.commerce.naver.com/external/v1/pay-order/seller-product-order/list', {
    headers: {
      'X-Naver-Client-Id': clientId,
      'X-Naver-Client-Secret': clientSecret
    },
    params: {
      lastChangedFrom: startDate.toISOString(),
      lastChangedTo: endDate.toISOString()
    }
  });
  
  // 응답 파싱
  const orders = response.data.data.lastChangeStatuses;
  
  let totalRevenue = 0;
  let orderCount = 0;
  
  for (const order of orders) {
    totalRevenue += order.totalPaymentAmount;
    orderCount++;
  }
  
  return {
    revenue: totalRevenue,
    orders: orderCount,
    avgOrderValue: orderCount > 0 ? Math.floor(totalRevenue / orderCount) : 0,
    source: 'naver',
    fetchedAt: new Date().toISOString()
  };
}
```

### 의존성 추가

```bash
cd /Users/mupeng/.openclaw/workspace/skills/daily-sales-digest
npm init -y
npm install axios
```

### 참고 문서

- [네이버 커머스 API](https://developer.naver.com/docs/commerce/commerce-api/commerce-api.md)
- [주문 조회 API](https://developer.naver.com/docs/commerce/commerce-api/commerce-api.md#%EC%A3%BC%EB%AC%B8-%EC%A1%B0%ED%9A%8C)

## 2. 쿠팡 Wing API

### API 키 발급

1. [쿠팡 Wing 개발자](https://wing-developers.coupang.com/) 로그인
2. 업체 등록
3. Access Key, Secret Key 발급

### 구현 (scripts/collect.js)

```javascript
async function collectCoupang(config, date) {
  if (!config.sources.coupang.enabled) {
    return null;
  }
  
  console.log('📦 쿠팡 데이터 수집 중...');
  
  const crypto = require('crypto');
  const axios = require('axios');
  
  const accessKey = config.sources.coupang.accessKey;
  const secretKey = config.sources.coupang.secretKey;
  const vendorId = config.sources.coupang.vendorId;
  
  // Wing API 인증 헤더 생성
  const datetime = new Date().toISOString();
  const path = `/v2/providers/wing_api/apis/api/v4/vendors/${vendorId}/ordersheets`;
  const message = datetime + 'GET' + path;
  const signature = crypto.createHmac('sha256', secretKey)
    .update(message)
    .digest('hex');
  
  const authHeader = `CEA algorithm=HmacSHA256, access-key=${accessKey}, signed-date=${datetime}, signature=${signature}`;
  
  // API 호출
  const response = await axios.get(`https://api-gateway.coupang.com${path}`, {
    headers: {
      'Authorization': authHeader,
      'Content-Type': 'application/json;charset=UTF-8'
    },
    params: {
      createdAtFrom: formatDate(date) + 'T00:00:00',
      createdAtTo: formatDate(date) + 'T23:59:59'
    }
  });
  
  // 응답 파싱
  const orders = response.data.data;
  
  let totalRevenue = 0;
  let orderCount = 0;
  
  for (const order of orders) {
    totalRevenue += order.paidPrice;
    orderCount++;
  }
  
  return {
    revenue: totalRevenue,
    orders: orderCount,
    avgOrderValue: orderCount > 0 ? Math.floor(totalRevenue / orderCount) : 0,
    source: 'coupang',
    fetchedAt: new Date().toISOString()
  };
}
```

### 참고 문서

- [쿠팡 Wing API](https://wing-developers.coupang.com/)
- [인증 가이드](https://wing-developers.coupang.com/hc/ko/articles/360033503973)

## 3. 배민셀러 API

배민셀러 API는 공개 문서가 제한적입니다. 배민 담당자에게 API 문서를 요청하세요.

### 일반적인 구조

```javascript
async function collectBaemin(config, date) {
  if (!config.sources.baemin.enabled) {
    return null;
  }
  
  console.log('📦 배민셀러 데이터 수집 중...');
  
  const axios = require('axios');
  const apiKey = config.sources.baemin.apiKey;
  const shopId = config.sources.baemin.shopId;
  
  // API 엔드포인트는 배민 제공 문서 참고
  const response = await axios.get('https://api.baemin.com/v1/sales', {
    headers: {
      'Authorization': `Bearer ${apiKey}`
    },
    params: {
      shopId,
      date: formatDate(date)
    }
  });
  
  const data = response.data;
  
  return {
    revenue: data.totalRevenue,
    orders: data.orderCount,
    avgOrderValue: data.avgOrderValue,
    source: 'baemin',
    fetchedAt: new Date().toISOString()
  };
}
```

## 4. 커스텀 POS 시스템

### REST API 연동

```javascript
async function collectPOS(config, date) {
  if (!config.sources.pos.enabled) {
    return null;
  }
  
  console.log('📦 POS 시스템 데이터 수집 중...');
  
  const axios = require('axios');
  const endpoint = config.sources.pos.endpoint;
  const apiKey = config.sources.pos.apiKey;
  
  const response = await axios.get(endpoint, {
    headers: apiKey ? { 'X-API-Key': apiKey } : {},
    params: {
      date: formatDate(date)
    }
  });
  
  const data = response.data;
  
  return {
    revenue: data.revenue,
    orders: data.orders,
    avgOrderValue: data.avgOrderValue || Math.floor(data.revenue / data.orders),
    source: 'pos',
    fetchedAt: new Date().toISOString()
  };
}
```

### POS API 서버 예시 (Node.js + Express)

```javascript
// pos-api-server.js
const express = require('express');
const app = express();

// 간단한 인증
const API_KEY = 'your-secret-api-key';

app.get('/api/sales', (req, res) => {
  const apiKey = req.headers['x-api-key'];
  
  if (apiKey !== API_KEY) {
    return res.status(401).json({ error: 'Unauthorized' });
  }
  
  const date = req.query.date; // YYYY-MM-DD
  
  // DB 조회 (예시)
  // const sales = db.query('SELECT * FROM sales WHERE date = ?', [date]);
  
  // Mock 데이터
  res.json({
    date,
    revenue: 1500000,
    orders: 45,
    avgOrderValue: 33333
  });
});

app.listen(3000, () => {
  console.log('POS API 서버 실행 중: http://localhost:3000');
});
```

## 5. 에러 처리

모든 API 호출에 에러 처리를 추가하세요:

```javascript
async function collectNaver(config, date) {
  if (!config.sources.naver.enabled) {
    return null;
  }
  
  try {
    console.log('📦 네이버 스마트스토어 데이터 수집 중...');
    
    // API 호출 로직...
    
    return {
      revenue: totalRevenue,
      orders: orderCount,
      avgOrderValue: avgOrderValue,
      source: 'naver',
      fetchedAt: new Date().toISOString()
    };
    
  } catch (error) {
    console.error('❌ 네이버 API 에러:', error.message);
    
    // 부분 실패 허용 (다른 소스는 계속 수집)
    return null;
    
    // 또는 전체 실패
    // throw error;
  }
}
```

## 6. 레이트 리밋 처리

API 호출 제한이 있는 경우 재시도 로직 추가:

```javascript
async function apiCallWithRetry(fn, retries = 3, delay = 1000) {
  for (let i = 0; i < retries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (error.response?.status === 429 && i < retries - 1) {
        console.log(`⏳ 레이트 리밋 초과. ${delay}ms 대기 후 재시도...`);
        await new Promise(resolve => setTimeout(resolve, delay));
        delay *= 2; // 지수 백오프
      } else {
        throw error;
      }
    }
  }
}

// 사용
const data = await apiCallWithRetry(() => 
  axios.get(url, { headers })
);
```

## 7. 테스트

API 연동 후 반드시 테스트:

```bash
# 개별 소스 테스트
node scripts/collect.js --date yesterday --source naver
node scripts/collect.js --date yesterday --source coupang
node scripts/collect.js --date yesterday --source baemin
node scripts/collect.js --date yesterday --source pos

# 전체 소스 테스트
node scripts/collect.js --date yesterday

# 데이터 확인
cat ~/.openclaw/workspace/data/sales/$(date -v-1d +%Y-%m-%d).json
```

## 8. 보안 체크리스트

- [ ] API 키는 절대 코드에 하드코딩하지 않음
- [ ] config 파일을 .gitignore에 추가
- [ ] HTTPS만 사용 (HTTP 금지)
- [ ] API 키 권한을 최소화 (읽기 전용)
- [ ] 로그에 민감한 정보 출력 금지
- [ ] 정기적으로 API 키 갱신

## 9. package.json 예시

```json
{
  "name": "daily-sales-digest",
  "version": "1.0.0",
  "description": "일일 매출 요약 스킬",
  "main": "scripts/collect.js",
  "scripts": {
    "collect": "node scripts/collect.js",
    "digest": "node scripts/digest.js",
    "alert": "node scripts/alert.js"
  },
  "dependencies": {
    "axios": "^1.6.0"
  },
  "devDependencies": {},
  "engines": {
    "node": ">=18.0.0"
  }
}
```

## 10. 다음 단계

API 연동 후:

1. 실제 데이터로 요약 테스트
2. cron 스케줄 설정
3. 알림 채널 테스트
4. 일주일간 모니터링
5. 피드백 수집 및 개선
