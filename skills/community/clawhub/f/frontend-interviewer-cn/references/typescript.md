# TypeScript 进阶面试题库

## 目录
- [初级](#初级)
- [中级](#中级)
- [高级](#高级)
- [专家](#专家)

---

## 初级

### TS-J-01 TypeScript 的核心优势
**难度：** 初级

**要点：**
- 静态类型检查，编译期捕获错误
- 更好的 IDE 支持（自动补全、重构）
- 类型即文档，提升代码可读性
- 渐进式采用，兼容 JavaScript

**追问：** TypeScript 的类型是强类型还是弱类型？（结构化类型系统 Structural Typing，duck typing）

---

### TS-J-02 interface vs type 的区别
**难度：** 初级

| 特性 | interface | type |
|------|-----------|------|
| 声明合并 | ✅ 支持 | ❌ 不支持 |
| 扩展语法 | `extends` | `&` 交叉类型 |
| 基础类型别名 | ❌ | ✅ `type ID = string` |
| 联合类型 | ❌ | ✅ `type A = B \| C` |
| 计算属性 | 有限支持 | ✅ 完全支持 |
| 映射类型 | ❌ | ✅ |

**最佳实践：** 公共 API 用 interface（支持声明合并），内部实现用 type（更灵活）

---

## 中级

### TS-M-01 泛型（Generics）深度解析
**难度：** 中级

**泛型约束：**
```typescript
// 约束泛型必须有 length 属性
function getLength<T extends { length: number }>(arg: T): number {
  return arg.length;
}

// 泛型类
class Stack<T> {
  private items: T[] = [];
  push(item: T) { this.items.push(item); }
  pop(): T | undefined { return this.items.pop(); }
}

// 泛型工厂函数
function create<T>(ctor: new () => T): T {
  return new ctor();
}
```

**条件类型（Conditional Types）：**
```typescript
type IsArray<T> = T extends any[] ? true : false;
type IsString = IsArray<string>; // false
type IsNumbers = IsArray<number[]>; // true

// infer 关键字提取类型
type ReturnType<T> = T extends (...args: any[]) => infer R ? R : never;
type UnpackPromise<T> = T extends Promise<infer U> ? U : T;
```

---

### TS-M-02 内置工具类型（Utility Types）
**难度：** 中级

```typescript
// Partial - 所有属性变为可选
type Partial<T> = { [P in keyof T]?: T[P]; }

// Required - 所有属性变为必须
type Required<T> = { [P in keyof T]-?: T[P]; }

// Readonly - 所有属性变为只读
type Readonly<T> = { readonly [P in keyof T]: T[P]; }

// Pick - 选取部分属性
type Pick<T, K extends keyof T> = { [P in K]: T[P]; }

// Omit - 排除部分属性
type Omit<T, K extends keyof T> = Pick<T, Exclude<keyof T, K>>;

// Record - 构建对象类型
type Record<K extends string, V> = { [P in K]: V; }

// Exclude - 从联合类型中排除
type Exclude<T, U> = T extends U ? never : T;

// Extract - 从联合类型中提取
type Extract<T, U> = T extends U ? T : never;

// NonNullable - 排除 null 和 undefined
type NonNullable<T> = T extends null | undefined ? never : T;
```

**面试常见手写：**
```typescript
// 手写 DeepReadonly
type DeepReadonly<T> = {
  readonly [P in keyof T]: T[P] extends object ? DeepReadonly<T[P]> : T[P];
};

// 手写 DeepPartial
type DeepPartial<T> = {
  [P in keyof T]?: T[P] extends object ? DeepPartial<T[P]> : T[P];
};
```

---

### TS-M-03 映射类型与模板字面量类型
**难度：** 中级/高级

**映射类型：**
```typescript
// 键值转换
type MappedType<T> = {
  [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K];
};

interface User { name: string; age: number; }
type UserGetters = MappedType<User>;
// { getName: () => string; getAge: () => number; }
```

**模板字面量类型：**
```typescript
type EventName<T extends string> = `on${Capitalize<T>}`;
type ClickEvent = EventName<'click'>; // 'onClick'

// 组合使用
type CSSProperty = `${string}-${string}`;
type BEM<B extends string, E extends string, M extends string> =
  `${B}__${E}--${M}`;
```

---

## 高级

### TS-S-01 装饰器（Decorators）
**难度：** 高级  
**考察点：** 元编程、AOP

**装饰器类型：**
```typescript
// 类装饰器
function Sealed(constructor: Function) {
  Object.seal(constructor);
  Object.seal(constructor.prototype);
}

// 方法装饰器
function Log(target: any, key: string, descriptor: PropertyDescriptor) {
  const original = descriptor.value;
  descriptor.value = function(...args: any[]) {
    console.log(`Calling ${key} with`, args);
    const result = original.apply(this, args);
    console.log(`${key} returned`, result);
    return result;
  };
  return descriptor;
}

// 属性装饰器
function Validate(target: any, key: string) {
  let value: string;
  Object.defineProperty(target, key, {
    get: () => value,
    set: (newVal: string) => {
      if (!newVal) throw new Error(`${key} cannot be empty`);
      value = newVal;
    }
  });
}

@Sealed
class UserService {
  @Validate name: string;
  
  @Log
  createUser(name: string) { return { id: Date.now(), name }; }
}
```

**执行顺序（由下至上，由内至外）：**
1. 参数装饰器
2. 方法/属性装饰器（从下到上）
3. 类装饰器

---

### TS-S-02 类型体操（Type Gymnastics）高频题
**难度：** 高级/专家

```typescript
// 1. 实现 TupleToUnion
type TupleToUnion<T extends any[]> = T[number];
type Colors = TupleToUnion<['red', 'green', 'blue']>; // 'red' | 'green' | 'blue'

// 2. 实现 UnionToIntersection
type UnionToIntersection<U> =
  (U extends any ? (x: U) => void : never) extends (x: infer I) => void ? I : never;

// 3. 实现 IsNever
type IsNever<T> = [T] extends [never] ? true : false;

// 4. 实现链式调用类型
interface Chainable<Option = {}> {
  option<K extends string, V>(
    key: K,
    value: V
  ): Chainable<Option & Record<K, V>>;
  get(): Option;
}

// 5. 实现 Permutation（全排列）
type Permutation<T, K = T> =
  [T] extends [never]
    ? []
    : K extends K
      ? [K, ...Permutation<Exclude<T, K>>]
      : never;

// 6. 递归类型 - 展平数组
type Flatten<T> = T extends (infer U)[]
  ? U extends any[]
    ? Flatten<U>
    : U
  : T;
```

---

## 专家

### TS-E-01 TypeScript 编译器与性能
**难度：** 专家

**tsconfig.json 关键配置：**
```json
{
  "compilerOptions": {
    "strict": true,              // 开启所有严格检查
    "noUncheckedIndexedAccess": true, // 索引访问包含 undefined
    "exactOptionalPropertyTypes": true, // 可选属性不能设为 undefined
    "isolatedModules": true,     // 每个文件独立编译（Vite/SWC 要求）
    "verbatimModuleSyntax": true, // 替代 importsNotUsedAsValues
    "skipLibCheck": true,        // 跳过 .d.ts 检查（加快编译）
    "incremental": true          // 增量编译
  }
}
```

**性能优化策略：**
1. 使用 `isolatedModules` + SWC/esbuild 加速开发
2. `Project References` 实现大型项目模块化编译
3. 避免大量复杂的条件类型（编译期计算开销）
4. 使用 `@ts-ignore` / `@ts-expect-error` 处理已知问题点

**追问：** TypeScript 5.x 的重要新特性？
- `const` 类型参数（TS 5.0）
- `using` 声明（Explicit Resource Management）（TS 5.2）
- 装饰器规范（ES TC39 Stage 3）（TS 5.0）
- `satisfies` 操作符（TS 4.9）
