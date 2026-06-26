# 高级表单模式

## 先判断是否需要表单库

- 1-3 个字段、无复杂校验、无动态字段、无组件库适配压力的表单，可用框架原生状态、浏览器约束校验和轻量提交状态。
- 需要动态字段、跨字段校验、多步流程、文件上传、异步校验、服务端错误回填或明显输入卡顿时，再引入专门表单方案。
- 表单库只管理字段状态和校验流程，不替代 API 错误映射、权限判断、可访问性标注或服务端最终校验。

## 选型参考

先沿用项目已有表单库、schema 库和组件库适配方式；新增依赖时再按场景选择。

| 场景 | 候选方案 | 注意点 |
| --- | --- | --- |
| React 复杂表单 | React Hook Form + Zod | 非受控优先，第三方受控组件用 `Controller`。 |
| Vue 复杂表单 | vee-validate / FormKit + Zod、Yup 或 Valibot | 不要为 Vue 项目引入 React-only 表单 API；优先沿用项目既有 Vue 表单库。 |
| 简单表单 | 框架原生状态 + 基础校验 | 避免为了 1-3 个字段引入重型表单体系。 |
| 多步表单 | 分步 schema + 最终提交 schema | 明确跨步数据保存、返回上一步和最终校验策略。 |
| 文件上传 | 表单库字段状态 + `FormData` | 校验文件数量、大小、类型；不要把 `File` JSON 序列化。 |
| 异步校验 | 提交边界校验或 debounce 字段校验 | 避免每次键入请求；处理竞态和旧响应覆盖。 |

## 通用实现原则

- 运行时 schema 或校验函数负责外部输入边界；TypeScript 类型不能替代运行时校验。
- 默认值、reset 数据和服务端回填数据要形状一致，避免字段在受控/非受控之间切换。
- 字段错误要能映射到具体字段；全局错误用于提交失败、权限或服务不可用等非字段问题。
- 组件库适配层要透传 value、onChange、onBlur、name/ref 或等价字段注册能力。
- 提交时保护 loading、重复提交、取消/过期请求、服务端错误回填和成功后 reset。
- 文件上传使用 `FormData` 或直传流程，前端校验只做体验保护，服务端仍需最终校验。
- 性能优化优先使用字段级订阅、局部组件拆分和延迟校验，不要全表单 watch 后驱动整页重渲染。

## React Hook Form Controller

```tsx
<Controller
  name="role"
  control={control}
  rules={{ required: "请选择角色" }}
  render={({ field, fieldState }) => (
    <>
      <Select {...field} options={roleOptions} />
      {fieldState.error && <span role="alert">{fieldState.error.message}</span>}
    </>
  )}
/>
```

用于不暴露原生 `ref` 的 Select、DatePicker、RichEditor 等组件。

## React Hook Form 动态字段

```tsx
const { fields, append, remove } = useFieldArray({
  control,
  name: "contacts",
});

{fields.map((field, index) => (
  <div key={field.id}>
    <input {...register(`contacts.${index}.name`)} />
    <button type="button" onClick={() => remove(index)}>删除</button>
  </div>
))}
```

`key` 必须使用 `field.id`，不要使用数组 index。

## Zod 联动校验

```ts
const schema = z
  .object({
    password: z.string().min(8),
    confirmPassword: z.string().min(8),
  })
  .refine((data) => data.password === data.confirmPassword, {
    message: "两次密码不一致",
    path: ["confirmPassword"],
  });
```

## Zod 文件上传校验

```ts
const schema = z.object({
  avatar: z
    .instanceof(FileList)
    .refine((files) => files.length > 0, "请上传头像")
    .refine((files) => files[0]?.size <= 5 * 1024 * 1024, "文件大小不超过 5MB")
    .refine((files) => ["image/jpeg", "image/png"].includes(files[0]?.type), "仅支持 JPG/PNG"),
});
```

提交时用 `FormData`，不要把 `File` JSON 序列化。

## 性能

- 用 `useWatch` 或字段级订阅替代全表单 watch。
- 大表单拆成 memoized 子组件或框架等价的局部更新单元。
- 高频输入不要每次键入触发网络校验。
- 多步表单要明确每步 schema 和跨步最终 schema。
