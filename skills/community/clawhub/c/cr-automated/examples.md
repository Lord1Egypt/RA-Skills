# Code Review Examples

実際のコードレビューシナリオと、期待されるフィードバックの例を示します。

## Example 0: CI失敗を含むPRレビュー

### シナリオ

PR #123をレビュー中。CI/CDチェックが複数失敗している。

### CI確認コマンド

```bash
$ gh pr checks 123

Some checks were not successful
X test          Test Suite                       1m23s  https://github.com/.../123
X build         Build                            45s    https://github.com/.../123
✓ lint          ESLint                           12s    https://github.com/.../123
✓ type-check    TypeScript Check                 8s     https://github.com/.../123
```

### 詳細確認

```bash
# テスト失敗の詳細
$ gh run view 987654321 --log-failed

FAIL src/auth/login.test.ts
  ● LoginService › should reject invalid credentials

    expect(received).rejects.toThrow(expected)

    Expected: "Invalid username or password"
    Received: "User not found"

      at Object.<anonymous> (src/auth/login.test.ts:45:5)

# ビルドエラーの詳細
$ gh run view 987654322 --log-failed

src/api/user.ts:42:15 - error TS2339: Property 'email' does not exist on type 'User'.

42     return user.email;
                 ~~~~~
```

### 自分のPRの場合のレビューと修正

**ステップ1: CI失敗の分析**
```bash
# ローカルでテスト実行
$ npm test -- src/auth/login.test.ts

# エラー内容から、エラーメッセージの変更が原因と判明
# テストの期待値を更新する必要がある
```

**ステップ2: 修正実施**

```typescript
// src/auth/login.test.ts (修正前)
it('should reject invalid credentials', async () => {
  await expect(login('invalid', 'password'))
    .rejects.toThrow('User not found'); // 古い期待値
});

// src/auth/login.test.ts (修正後)
it('should reject invalid credentials', async () => {
  await expect(login('invalid', 'password'))
    .rejects.toThrow('Invalid username or password'); // 新しい期待値
});

// src/api/user.ts (ビルドエラー修正)
// User型にemailプロパティを追加
interface User {
  id: string;
  username: string;
  email: string; // 追加
  passwordHash: string;
}
```

**ステップ3: ローカルで検証**
```bash
$ npm run type-check
✓ No TypeScript errors

$ npm test
✓ All tests passed (15 tests)

$ npm run build
✓ Build successful
```

**ステップ4: コミット・プッシュ**
```bash
$ git add .
$ git commit -m "fix: resolve CI failures

- Update test expectations for new error messages
- Add email property to User type"
$ git push
```

### 他人のPRの場合のレビューコメント

```markdown
## コードレビュー結果: PR #123

### ⚠️ CI/CD Status

現在、以下のCI/CDチェックが失敗しています:

#### ❌ Test Suite Failures

**失敗テスト**: `src/auth/login.test.ts:45` - "should reject invalid credentials"

**原因**:
エラーメッセージを`"User not found"`から`"Invalid username or password"`に変更したため、
テストの期待値が一致しなくなっています。

**修正方法**:
```typescript
// src/auth/login.test.ts:45
it('should reject invalid credentials', async () => {
  await expect(login('invalid', 'password'))
    .rejects.toThrow('Invalid username or password'); // 変更
});
```

これは良い変更です(アカウント列挙攻撃対策)が、テストの更新が必要です。

#### ❌ Build Error

**エラー**: `src/api/user.ts:42:15` - Property 'email' does not exist on type 'User'

**原因**:
User型の定義に`email`プロパティが含まれていません。

**修正方法**:
```typescript
// types/user.ts または該当ファイル
interface User {
  id: string;
  username: string;
  email: string;        // 追加
  passwordHash: string;
}
```

---

### 🟡 Warnings

**1. エラーハンドリングの改善が必要**
- src/auth/login.ts:25 - セッションIDの生成に`Math.random()`使用
  - 暗号学的に安全な`crypto.randomBytes()`を推奨

### 🟢 Good Practices

**1. セキュリティ向上**
- エラーメッセージの統一によるアカウント列挙対策 ✓
- 適切なbcrypt使用 ✓

### 📝 Notes

CI修正後、再度レビュー依頼をお願いします。
```

## Example 0-2: 自分のPRでセキュリティスキャン失敗

### CI確認

```bash
$ gh pr checks

Some checks were not successful
X security-scan  CodeQL / Analyze              2m15s  https://github.com/.../run/...
✓ test          Test Suite                     1m10s  https://github.com/.../run/...
✓ build         Build                          52s    https://github.com/.../run/...
```

### 詳細確認

```bash
$ gh pr view 456 --json statusCheckRollup --jq '.statusCheckRollup[] | select(.conclusion == "FAILURE")'

{
  "name": "CodeQL / Analyze",
  "conclusion": "FAILURE",
  "detailsUrl": "https://github.com/.../security/code-scanning/..."
}
```

### GitHub Security Alertsで確認

セキュリティタブで以下の警告を確認:

```
SQL Injection vulnerability
Severity: High
CWE-89: Improper Neutralization of Special Elements used in an SQL Command

Location: src/db/users.ts:15
```

### 修正実施

```typescript
// src/db/users.ts (修正前 - SQL Injection脆弱性)
export async function findUserByName(name: string) {
  const query = `SELECT * FROM users WHERE name = '${name}'`; // 危険!
  return db.execute(query);
}

// src/db/users.ts (修正後 - Parameterized query)
export async function findUserByName(name: string) {
  const query = 'SELECT * FROM users WHERE name = ?';
  return db.execute(query, [name]); // 安全
}
```

### 検証とプッシュ

```bash
# ローカルでセキュリティチェック（CodeQLは重いのでlinter系で代用）
$ npm run lint:security  # または eslint-plugin-security など

# 修正をコミット
$ git add src/db/users.ts
$ git commit -m "fix: resolve SQL injection vulnerability (CWE-89)

Replace string interpolation with parameterized query
to prevent SQL injection attacks."
$ git push

# CIの再実行を待つ
$ gh pr checks --watch
```

## Example 1: セキュリティ問題

### レビュー対象コード

```typescript
// src/auth/login.ts
import bcrypt from 'bcrypt';

const ADMIN_PASSWORD = "admin123"; // ハードコード

export async function login(username: string, password: string) {
  const user = await db.users.findOne({ username });

  if (!user) {
    throw new Error("User not found");
  }

  // パスワード比較
  const isValid = await bcrypt.compare(password, user.passwordHash);

  if (isValid) {
    // セッション作成
    const sessionId = Math.random().toString(36); // 脆弱な乱数
    await db.sessions.create({ userId: user.id, sessionId });

    return { sessionId };
  }

  throw new Error("Invalid password");
}
```

### レビューフィードバック

```markdown
## コードレビュー結果: src/auth/login.ts

### 🔴 Critical Issues

**1. ハードコードされた認証情報**
- **場所**: line 4
- **問題**: 管理者パスワードがソースコードに直接記述されています
- **影響**: コードが漏洩した場合、即座に悪用される可能性があります
- **修正方法**:
  ```typescript
  const ADMIN_PASSWORD = process.env.ADMIN_PASSWORD;
  if (!ADMIN_PASSWORD) {
    throw new Error('ADMIN_PASSWORD must be set');
  }
  ```
- **追加対応**: .gitに既にコミットされている場合は、Git履歴から削除し、パスワードを変更してください

**2. 脆弱な乱数生成**
- **場所**: line 18
- **問題**: `Math.random()`は暗号学的に安全ではありません
- **影響**: セッションIDが予測可能になり、セッションハイジャックのリスクがあります
- **修正方法**:
  ```typescript
  import { randomBytes } from 'crypto';
  const sessionId = randomBytes(32).toString('hex');
  ```

### 🟡 Warnings

**3. 情報漏洩のリスク**
- **場所**: line 10, 24
- **問題**: エラーメッセージでユーザーの存在を判別可能
- **影響**: アカウント列挙攻撃に利用される可能性
- **修正方法**:
  ```typescript
  // 両方のケースで同じエラーメッセージ
  throw new Error("Invalid username or password");
  ```

**4. タイミング攻撃への脆弱性**
- **問題**: ユーザー存在確認とパスワード検証で処理時間が異なる
- **提案**: 常に同じ処理時間になるよう、ダミーのbcrypt比較を実行

### 💡 Suggestions

**5. レート制限の追加**
```typescript
import rateLimit from 'express-rate-limit';

const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15分
  max: 5 // 最大5回まで
});
```

**6. ログイン試行の記録**
- 失敗したログイン試行を記録し、不審なアクティビティを検出
```

## Example 2: パフォーマンス問題

### レビュー対象コード

```typescript
// src/api/posts.ts
export async function getPostsWithComments(userId: string) {
  const posts = await db.posts.findMany({
    where: { authorId: userId }
  });

  const result = [];
  for (const post of posts) {
    const comments = await db.comments.findMany({
      where: { postId: post.id }
    });

    const enrichedComments = [];
    for (const comment of comments) {
      const author = await db.users.findUnique({
        where: { id: comment.authorId }
      });

      enrichedComments.push({
        ...comment,
        authorName: author.name
      });
    }

    result.push({
      ...post,
      comments: enrichedComments
    });
  }

  return result;
}
```

### レビューフィードバック

```markdown
## コードレビュー結果: src/api/posts.ts

### 🔴 Critical Issues

**1. N+1クエリ問題 (複数箇所)**
- **場所**: line 9-11, 15-17
- **問題**:
  - posts配列の各要素に対してcommentsをクエリ (N回)
  - comments配列の各要素に対してusersをクエリ (N*M回)
  - 例: 10件の投稿、各5コメント = 1 + 10 + 50 = 61クエリ
- **影響**: データ量が増えると指数関数的にパフォーマンスが悪化
- **修正方法**:

```typescript
export async function getPostsWithComments(userId: string) {
  // 1回のクエリで全データ取得
  const posts = await db.posts.findMany({
    where: { authorId: userId },
    include: {
      comments: {
        include: {
          author: true
        }
      }
    }
  });

  // データ整形のみ
  return posts.map(post => ({
    ...post,
    comments: post.comments.map(comment => ({
      ...comment,
      authorName: comment.author.name
    }))
  }));
}
```

### 💡 Suggestions

**2. ページネーションの追加**
```typescript
export async function getPostsWithComments(
  userId: string,
  options: { page?: number; limit?: number } = {}
) {
  const page = options.page || 1;
  const limit = options.limit || 20;
  const skip = (page - 1) * limit;

  const [posts, total] = await Promise.all([
    db.posts.findMany({
      where: { authorId: userId },
      include: { comments: { include: { author: true } } },
      skip,
      take: limit
    }),
    db.posts.count({ where: { authorId: userId } })
  ]);

  return {
    posts,
    pagination: {
      page,
      limit,
      total,
      totalPages: Math.ceil(total / limit)
    }
  };
}
```

**3. キャッシング戦略**
- よく閲覧される投稿はRedisにキャッシュすることを検討
- TTL: 5分程度が適切か
```

## Example 3: テストの不備

### レビュー対象コード

```typescript
// src/utils/validator.test.ts
import { validateEmail } from './validator';

describe('validateEmail', () => {
  it('should work', () => {
    expect(validateEmail('test@example.com')).toBe(true);
  });
});
```

### レビューフィードバック

```markdown
## コードレビュー結果: src/utils/validator.test.ts

### 🟡 Warnings

**1. 不十分なテストカバレッジ**
- **問題**: 正常系の1ケースのみで、エッジケースやエラーケースがテストされていません
- **提案**: 以下のケースを追加してください

```typescript
describe('validateEmail', () => {
  describe('valid emails', () => {
    it('should accept standard email format', () => {
      expect(validateEmail('test@example.com')).toBe(true);
    });

    it('should accept email with subdomain', () => {
      expect(validateEmail('user@mail.example.com')).toBe(true);
    });

    it('should accept email with plus addressing', () => {
      expect(validateEmail('user+tag@example.com')).toBe(true);
    });
  });

  describe('invalid emails', () => {
    it('should reject email without @', () => {
      expect(validateEmail('invalid.email.com')).toBe(false);
    });

    it('should reject email without domain', () => {
      expect(validateEmail('user@')).toBe(false);
    });

    it('should reject email with spaces', () => {
      expect(validateEmail('user @example.com')).toBe(false);
    });

    it('should reject empty string', () => {
      expect(validateEmail('')).toBe(false);
    });
  });

  describe('edge cases', () => {
    it('should handle null gracefully', () => {
      expect(validateEmail(null as any)).toBe(false);
    });

    it('should handle undefined gracefully', () => {
      expect(validateEmail(undefined as any)).toBe(false);
    });

    it('should handle very long email', () => {
      const longEmail = 'a'.repeat(300) + '@example.com';
      expect(validateEmail(longEmail)).toBe(false);
    });
  });
});
```

**2. テストの説明が不明確**
- `'should work'` は何が期待されるのか不明
- 各テストは期待される振る舞いを明確に記述すべき
```

## Example 4: 良いコード

### レビュー対象コード

```typescript
// src/services/payment.ts
import { z } from 'zod';
import Stripe from 'stripe';
import { logger } from '../utils/logger';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2023-10-16',
  typescript: true
});

const PaymentInputSchema = z.object({
  amount: z.number().positive().max(999999),
  currency: z.enum(['usd', 'eur', 'jpy']),
  customerId: z.string().min(1),
  idempotencyKey: z.string().uuid()
});

type PaymentInput = z.infer<typeof PaymentInputSchema>;

export class PaymentService {
  async createPayment(input: unknown): Promise<Stripe.PaymentIntent> {
    // 入力検証
    const validatedInput = PaymentInputSchema.parse(input);

    try {
      const paymentIntent = await stripe.paymentIntents.create(
        {
          amount: validatedInput.amount,
          currency: validatedInput.currency,
          customer: validatedInput.customerId,
          automatic_payment_methods: { enabled: true }
        },
        {
          idempotencyKey: validatedInput.idempotencyKey,
          timeout: 5000
        }
      );

      logger.info('Payment created', {
        paymentIntentId: paymentIntent.id,
        amount: validatedInput.amount,
        customerId: validatedInput.customerId
      });

      return paymentIntent;
    } catch (error) {
      logger.error('Payment creation failed', {
        error,
        customerId: validatedInput.customerId
      });

      if (error instanceof Stripe.errors.StripeError) {
        // Stripeエラーを適切に処理
        throw new PaymentError(
          `Payment failed: ${error.message}`,
          error.type
        );
      }

      throw error;
    }
  }
}
```

### レビューフィードバック

```markdown
## コードレビュー結果: src/services/payment.ts

### 🟢 Good Practices

**1. 適切な入力検証**
- Zodを使用した型安全な検証 (line 11-17)
- ランタイムとコンパイル時の両方で型安全性を確保

**2. セキュリティベストプラクティス**
- 環境変数からAPIキーを読み込み (line 6)
- Idempotency keyによる重複決済防止 (line 33)
- タイムアウト設定で長時間のハング防止 (line 34)

**3. 適切なエラーハンドリング**
- try-catchで例外を捕捉 (line 25)
- Stripe固有のエラーを識別して処理 (line 50-55)
- 詳細なログ出力 (line 37, 45)

**4. 保守性**
- TypeScriptの型定義を活用
- マジックナンバーなし
- 明確な関数名とパラメータ名

### 💡 Suggestions

**1. リトライメカニズムの追加**
ネットワークエラーなど一時的な障害に対するリトライがあるとより堅牢:

```typescript
import pRetry from 'p-retry';

async createPayment(input: unknown): Promise<Stripe.PaymentIntent> {
  const validatedInput = PaymentInputSchema.parse(input);

  return pRetry(
    () => stripe.paymentIntents.create(...),
    {
      retries: 3,
      onFailedAttempt: error => {
        logger.warn('Payment attempt failed, retrying...', { error });
      }
    }
  );
}
```

**2. テストの追加確認**
このコードは非常に良く書けていますが、以下のテストがあるか確認:
- [ ] 正常系のテスト
- [ ] バリデーションエラーのテスト
- [ ] Stripeエラーのモックテスト
- [ ] タイムアウトのテスト
```

## Example 5: プルリクエスト全体のレビュー

### シナリオ

ユーザー認証機能の追加PR:
- 5ファイル変更
- +320 -15行

### レビューフィードバック

```markdown
## PR Review: ユーザー認証機能の追加

### 📊 Summary
全体的によく設計された実装です。いくつかのセキュリティ改善と、テストの追加が必要です。

### 🔴 Critical Issues (2件)

1. **src/auth/password.ts:25** - パスワードハッシュのsalt roundsが不足
   - 現在: 8 → 推奨: 12以上

2. **src/middleware/auth.ts:42** - JWTシークレットがハードコード
   - 環境変数に移行が必要

### 🟡 Warnings (3件)

1. **src/routes/auth.ts:15** - レート制限がない
   - ブルートフォース攻撃への対策が必要

2. **src/auth/session.ts:30** - セッションタイムアウトが長すぎる(30日)
   - セキュリティリスクを考慮して7日程度に短縮を推奨

3. **tests/auth.test.ts** - エラーケースのテストが不足
   - 無効なトークン、期限切れトークンなどのテストを追加

### 🟢 Good Practices (4件)

1. bcryptを使用した適切なパスワードハッシング
2. JWTの使用とペイロード設計が適切
3. ミドルウェアの分離が明確
4. TypeScriptの型定義が充実

### 💡 Suggestions

1. リフレッシュトークンの実装を検討
2. 2FA(二要素認証)の将来的な追加を見据えた設計に
3. ログイン履歴の記録機能があると監査に有用

### ✅ Approval Status

**Changes Requested** - Criticalな問題2件の修正後にApprove可能です

### 📝 Next Steps

1. Criticalな問題を修正
2. セキュリティテストを追加
3. 再レビュー依頼
```

---

これらの例は、実際のコードレビュー時の参考として使用してください。プロジェクトの段階やコンテキストに応じて、適切なレベルの厳密さでレビューを実施することが重要です。
