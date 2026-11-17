/**
 * 最小工具插件骨架 —— T3 形态（让模型调用你的能力）
 *
 * 来源：
 *   - 官方文档 docs/user/develop/basic/tool.zh.md:11-33
 *   - 官方最小工具插件 packages/interaction/tool-ask-user（全包 101 行）
 *
 * 复制后要改的地方：插件名 name、工具名 name、description、parameters、execute。
 *
 * ⚠️ 绝对不要写 export default。函数式插件用命名导出；
 *    写了 default 会被 Loader 当成「服务类」解析，进而丢弃函数插件的命名空间。
 *
 * 为什么这个骨架是**纯 JavaScript、零构建**：
 *   「发布前必须构建好产物（lib/），因为 dsh 不会跑你的 build」
 *   （出处：本技能 references/06-workflow.md，对应上游 packages/… 的打包约定）。
 *   骨架默认让你免于踩「main 指向一个还没生成的 index.js」这个坑——
 *   它开箱即可 `dsh plugin add`。要用 TypeScript 的话见本目录 README 的「升级到 TS」。
 */

import { defineTool } from '@deepseek-ai/dsh-tools'

/** 插件名。全局唯一，建议与包名一致。 */
export const name = 'dsh-tool-greet'

/**
 * 声明依赖的服务。Cordis 会等这些服务就绪后再调用 apply。
 * 不写 'tools' 的话 ctx.tools 就是 undefined，插件直接报错。
 * 可选服务不要写在这里，改用 ctx.get('x') 取。
 */
export const inject = ['tools']

/** @param {import('@deepseek-ai/cordis').Context} ctx */
export function apply(ctx) {
  ctx.tools.register(defineTool({
    /** 模型看到的工具名：下划线风格，全局唯一。'run_code' 是保留名，不能用。 */
    name: 'greet',

    /**
     * 写给模型看的。模型靠它决定「要不要调用」，
     * 所以重点是讲清「什么时候用」，而不是讲实现细节。
     */
    description: 'Greet someone by name. '
      + 'Use this when the user asks to be greeted, or to verify that a custom tool is registered and reachable.',

    /**
     * DSH 自有 Schema DSL —— 注意和「裸 register 路径」写法不同：
     *   - 根是「隐式对象」，直接铺字段名，不要写 type:'object' / properties 包装
     *   - 必填写在**属性级**：required: true
     *     （裸 ctx.tools.register 才用对象级 required: ['name']。混用必报错。）
     *   - 支持的类型：string / number / integer / boolean / null / array / object / json，或 oneOf
     */
    parameters: {
      name: {
        type: 'string',
        required: true,
        description: 'The name to greet.',
      },
    },

    output: {
      /** 返回值结构约束。模型看到的就是它，别省。 */
      schema: { type: 'string' },
      /** 把规范值渲染成面向模型的内容块。 */
      render: (_args, value) => [{ type: 'text', text: value }],
    },

    /**
     * 业务逻辑。只返回**纯数据**（可序列化 JSON）：
     * 不要返回 undefined / 函数 / 类实例；unknown 要逐字段收窄。
     * exec.signal 是取消信号，exec.agent 是当前 agent。
     */
    async execute(args) {
      return `Hello, ${args.name}!`
    },
  }))
}

/* ────────────────────────────────────────────────────────────────
 * 复杂参数的写法（需要时把上面 parameters 换成这个形状）
 *
 *   parameters: {
 *     questions: {
 *       type: 'array',
 *       required: true,                       // ← 数组本身必填，同样是属性级
 *       description: 'Questions to ask the user before continuing.',
 *       items: {
 *         type: 'object',
 *         additionalProperties: true,
 *         properties: {
 *           id:       { type: 'string', required: true, description: 'Stable id; echoed in the answer.' },
 *           question: { type: 'string', required: true, description: 'The question to ask the user.' },
 *         },
 *       },
 *     },
 *   },
 *
 * 注意：output.schema 走 defineTool 时也是同一套 DSL，
 * 且它的**根节点不允许 required**。
 * ──────────────────────────────────────────────────────────────── */
