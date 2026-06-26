"""
LLM-Wiki 命令实现

与 Claude Code 集成的具体命令。
"""

from pathlib import Path
from typing import Optional
import click

from .agent_logger import setup_agent_logging, get_logger
from .config import load_config
from .core import WikiManager, find_wiki_root, IngestResult
from .embeddings import create_provider
from .linker import KnowledgeLinker
from .merge import ContentMerger, MergeStrategy, SafeWriter
from .retrieval import EmbeddingIndex

LOG = get_logger("commands")


@click.group()
@click.option('--wiki-dir', type=click.Path(), help='Wiki 目录路径')
@click.option('--verbose', '-v', is_flag=True, help='启用详细日志输出到 stderr')
@click.pass_context
def cli(ctx, wiki_dir: Optional[str], verbose: bool):
    """LLM-Wiki 命令行工具"""
    setup_agent_logging()
    if verbose:
        get_logger("").setLevel("DEBUG")

    if wiki_dir:
        root = Path(wiki_dir)
    else:
        root = find_wiki_root()

    if not root:
        click.echo("错误：找不到 wiki 根目录。请确保当前目录在 wiki 内，或指定 --wiki-dir")
        ctx.exit(1)

    LOG.info("CLI initialized: root=%s", root)
    ctx.ensure_object(dict)
    ctx.obj['wiki'] = WikiManager(root / "wiki")
    ctx.obj['root'] = root


@cli.command()
@click.argument('source_path', type=click.Path(exists=True))
@click.option('--dry-run', is_flag=True, help='预览但不实际修改')
@click.pass_context
def ingest(ctx, source_path: str, dry_run: bool):
    """
    摄取资料到 wiki

    示例：
        wiki ingest sources/paper.pdf
        wiki ingest sources/笔记.md --dry-run
    """
    wiki = ctx.obj['wiki']
    root = ctx.obj['root']
    source = Path(source_path)

    # 读取资料内容
    click.echo(f"正在读取: {source}")

    if dry_run:
        click.echo("【模拟模式】将执行以下操作：")
        click.echo(f"  - 分析 {source.name}")
        click.echo(f"  - 识别相关 wiki 页面")
        click.echo(f"  - 创建/更新页面")
        click.echo(f"  - 追加到 log.md")
        return

    # 实际逻辑由 LLM 通过工具调用完成
    # 这里只提供 CLI 接口
    click.echo(f"请使用自然语言指令：")
    click.echo(f'  "请摄入资料 {source.name} 到 wiki"')


@cli.command()
@click.argument('query_text')
@click.option('--save', is_flag=True, help='将回答保存为新页面')
@click.option('--semantic', is_flag=True, help='使用语义搜索（需要已建立 embedding 索引）')
@click.pass_context
def query(ctx, query_text: str, save: bool, semantic: bool):
    """
    查询 wiki 知识库

    示例：
        wiki query "Transformer 的工作原理"
        wiki query "LoRA 和全量微调的区别" --save
        wiki query "优化方法" --semantic
    """
    LOG.info("query: text=%s semantic=%s", query_text, semantic)
    wiki = ctx.obj['wiki']
    root = ctx.obj['root']

    click.echo(f"查询: {query_text}")

    config = load_config(root)
    use_semantic = semantic or (
        config.get('embedding', {}).get('enabled', False)
        and (root / 'wiki' / '.cache' / 'embeddings.json').exists()
    )

    if use_semantic:
        provider = create_provider(config)
        if provider is None:
            click.echo("\n错误：未找到有效的 embedding 配置。请检查 config.yaml")
            ctx.exit(1)

        index = EmbeddingIndex(wiki, provider)
        if not index.cache or not index.cache.get('pages'):
            click.echo("\n错误：embedding 索引为空。请先运行 `wiki index`")
            ctx.exit(1)

        retrieval_cfg = config.get('retrieval', {})
        results = index.search(
            query_text,
            top_k=retrieval_cfg.get('top_k', 10),
            keyword_weight=retrieval_cfg.get('keyword_weight', 0.3),
            vector_weight=retrieval_cfg.get('vector_weight', 0.5),
            link_weight=retrieval_cfg.get('link_weight', 0.2),
            enable_link_traversal=retrieval_cfg.get('enable_link_traversal', True),
        )

        if results:
            click.echo(f"\n语义检索结果（Top {len(results)}）：")
            for title, score in results:
                click.echo(f"  - {title:<30} (score: {score:.3f})")
        else:
            click.echo("\n未找到相关页面。")

        click.echo(f"\n请使用自然语言指令进一步分析：")
        click.echo(f'  "查询 wiki: {query_text}"')
        if save:
            click.echo(f'  （添加 --save 会将结果存档）')
        return

    # 列出可用页面供参考
    pages = wiki.list_pages()
    if pages:
        click.echo(f"\n当前 wiki 有 {len(pages)} 个页面:")
        for p in pages[:10]:
            click.echo(f"  - {p.title}")
        if len(pages) > 10:
            click.echo(f"  ... 还有 {len(pages) - 10} 个")

    click.echo(f"\n请使用自然语言指令：")
    click.echo(f'  "查询 wiki: {query_text}"')
    if save:
        click.echo(f'  （添加 --save 会将结果存档）')


@cli.command()
@click.option('--source', required=True, help='新页面标题')
@click.option('--target', help='目标已有页面标题（指定后执行合并而非仅报告）')
@click.option('--mode', type=click.Choice(['light', 'deep']), default='light',
              help='关联模式: light=仅报告, deep=包含内容融合建议')
@click.option('--strategy', type=click.Choice(['link_only', 'append_related', 'append_section', 'update_concept']),
              default='link_only', help='合并策略（仅当 --target 指定时生效）')
@click.option('--max-related', default=5, help='返回的最大关联数')
@click.option('--dry-run', is_flag=True, help='预览但不实际修改')
@click.option('--output-format', type=click.Choice(['markdown', 'json']), default='markdown',
              help='输出格式')
@click.pass_context
def link(ctx, source: str, target: Optional[str], mode: str, strategy: str,
         max_related: int, dry_run: bool, output_format: str):
    """
    关联新知识与已有 wiki 页面。

    单文件轻量关联（仅报告）：
        wiki link --source "NewPage" --mode light

    深度关联（含内容融合建议）：
        wiki link --source "NewPage" --mode deep

    执行具体合并（指定 --target）：
        wiki link --source "NewPage" --target "OldPage" --strategy append_related
    """
    LOG.info("link: source=%s target=%s mode=%s strategy=%s dry_run=%s",
             source, target, mode, strategy, dry_run)
    wiki = ctx.obj['wiki']
    root = ctx.obj['root']

    config = load_config(root)
    linking_cfg = config.get('linking', {})
    if not linking_cfg.get('enabled', True):
        click.echo("错误：关联功能已禁用。请在 config.yaml 中设置 linking.enabled: true")
        ctx.exit(1)

    # 获取 source 页面
    source_page = wiki.get_page(source)
    if not source_page:
        click.echo(f"错误：找不到源页面: {source}")
        ctx.exit(1)

    # 初始化关联引擎
    linker = KnowledgeLinker(wiki)
    if mode == 'deep':
        # 尝试使用 embedding 索引
        embedding_cfg = config.get('embedding', {})
        if embedding_cfg.get('enabled', False):
            try:
                provider = create_provider(config)
                if provider:
                    index = EmbeddingIndex(wiki, provider)
                    linker.index = index
                    LOG.info("Embedding index attached for deep mode")
            except Exception:
                LOG.warning("Embedding unavailable, falling back to keyword", exc_info=True)

    # 如果指定了 target，执行合并操作
    if target:
        target_page = wiki.get_page(target)
        if not target_page:
            click.echo(f"错误：找不到目标页面: {target}")
            ctx.exit(1)

        strategy_enum = MergeStrategy(strategy)

        # 检查策略是否被允许
        deep_cfg = linking_cfg.get('deep_mode', {})
        allowed = deep_cfg.get('strategies_allowed', [])
        if strategy not in allowed:
            click.echo(f"错误：策略 '{strategy}' 不在允许列表中。允许的策略: {', '.join(allowed)}")
            ctx.exit(1)

        merger = ContentMerger(wiki)
        context = {
            'target': source,
            'relation_desc': f"由 {source} 关联添加",
        }

        # 根据策略准备 addition
        if strategy_enum == MergeStrategy.APPEND_RELATED:
            addition = ""
        elif strategy_enum == MergeStrategy.APPEND_SECTION:
            addition = f"参见 [[{source}]] 中的最新分析。"
            context['section_title'] = '## 最新进展'
        else:
            addition = ""

        new_content = merger.merge(target_page, addition, strategy_enum, context)
        diff = merger.generate_diff(
            target_page.path.read_text(encoding='utf-8'),
            new_content,
        )

        if dry_run:
            click.echo(f"【模拟模式】将修改: {target}")
            click.echo(f"策略: {strategy}")
            click.echo("\nDiff:")
            click.echo(diff)
            return

        writer = SafeWriter(wiki)
        proposal = writer.prepare(
            target_page, new_content,
            reason=f"关联 {source} → {target}",
            strategy=strategy_enum,
        )

        # 如果深度模式要求审查，输出 diff 等待确认
        if mode == 'deep' and deep_cfg.get('require_diff_review', True):
            click.echo(f"变更提案: {target}")
            click.echo(proposal.to_markdown())
            click.echo("\n请审查 diff 后运行（不带 --dry-run）应用修改。")
            return

        backup = writer.apply(proposal)
        click.echo(f"[OK] 已更新 {target}")
        click.echo(f"  备份: {backup}")
        return

    # 未指定 target：执行关联发现，输出报告
    light_cfg = linking_cfg.get('light_mode', {})
    if mode == 'light':
        rels = linker.find_related(
            query=source,
            query_tags=source_page.tags,
            query_content=source_page.content,
            top_k=max_related,
            min_score=light_cfg.get('min_score', 0.3),
            use_embedding=light_cfg.get('vector_weight', 0) > 0,
            keyword_weight=light_cfg.get('keyword_weight', 0.6),
            vector_weight=light_cfg.get('vector_weight', 0.0),
            link_weight=light_cfg.get('link_weight', 0.4),
        )
    else:
        deep_cfg = linking_cfg.get('deep_mode', {})
        rels = linker.find_related(
            query=source,
            query_tags=source_page.tags,
            query_content=source_page.content,
            top_k=max_related,
            min_score=deep_cfg.get('min_score', 0.2),
            use_embedding=True,
            keyword_weight=0.4,
            vector_weight=0.4,
            link_weight=0.2,
        )

    graph = linker.build_relation_graph([source], mode=mode)

    if output_format == 'json':
        import json
        data = [
            {
                'source': r.source,
                'target': r.target,
                'score': r.score,
                'relation_type': r.relation_type.value,
                'evidence': r.evidence,
                'suggested_action': r.suggested_action,
            }
            for r in rels
        ]
        click.echo(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        click.echo(graph.to_markdown(title=f"关联报告: {source}"))


@cli.command()
@click.option('--since', help='自某日期（YYYY-MM-DD）以来的新页面')
@click.option('--mode', type=click.Choice(['light', 'deep']), default='deep',
              help='关联模式')
@click.option('--dry-run', is_flag=True, help='预览但不实际修改')
@click.option('--output-format', type=click.Choice(['markdown', 'json']), default='markdown')
@click.pass_context
def relink(ctx, since: Optional[str], mode: str, dry_run: bool, output_format: str):
    """
    全局深度关联：对近期新增页面执行全局关联更新。

    对指定日期后新增的所有页面，分析其与整个 wiki 的关系网络。

    示例：
        wiki relink --since 2026-04-20 --mode deep
        wiki relink --since 2026-04-20 --dry-run
    """
    LOG.info("relink: since=%s mode=%s dry_run=%s", since, mode, dry_run)
    wiki = ctx.obj['wiki']
    root = ctx.obj['root']

    config = load_config(root)
    linking_cfg = config.get('linking', {})
    if not linking_cfg.get('enabled', True):
        click.echo("错误：关联功能已禁用。请在 config.yaml 中设置 linking.enabled: true")
        ctx.exit(1)

    # 筛选新页面
    all_pages = wiki.list_pages()
    if since:
        try:
            from datetime import datetime as dt
            since_date = dt.strptime(since, '%Y-%m-%d')
            new_pages = [
                p for p in all_pages
                if p.frontmatter.get('created')
                and dt.strptime(str(p.frontmatter.get('created')), '%Y-%m-%d') >= since_date
            ]
        except ValueError:
            click.echo(f"错误：日期格式无效: {since}。请使用 YYYY-MM-DD 格式。")
            ctx.exit(1)
    else:
        # 默认取最近 7 天
        from datetime import datetime as dt, timedelta
        cutoff = dt.now() - timedelta(days=7)
        new_pages = [
            p for p in all_pages
            if p.frontmatter.get('created')
            and dt.strptime(str(p.frontmatter.get('created')), '%Y-%m-%d') >= cutoff
        ]

    if not new_pages:
        click.echo("未找到需要关联的新页面。")
        return

    click.echo(f"发现 {len(new_pages)} 个新页面，执行 {mode} 模式关联...\n")

    # 初始化关联引擎
    linker = KnowledgeLinker(wiki)
    if mode == 'deep':
        embedding_cfg = config.get('embedding', {})
        if embedding_cfg.get('enabled', False):
            try:
                provider = create_provider(config)
                if provider:
                    index = EmbeddingIndex(wiki, provider)
                    linker.index = index
            except Exception:
                pass

    new_page_titles = [p.title for p in new_pages]
    graph = linker.build_relation_graph(
        new_page_titles,
        mode=mode,
        top_k=linking_cfg.get('deep_mode', {}).get('top_k', 10) if mode == 'deep'
        else linking_cfg.get('light_mode', {}).get('top_k', 5),
    )

    if dry_run:
        click.echo("【模拟模式】关联报告:")

    if output_format == 'json':
        import json
        data = [
            {
                'source': r.source,
                'target': r.target,
                'score': r.score,
                'relation_type': r.relation_type.value,
                'evidence': r.evidence,
                'suggested_action': r.suggested_action,
            }
            for r in graph.relations
        ]
        click.echo(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        click.echo(graph.to_markdown(title=f"全局关联报告 ({mode} 模式)"))

    if not dry_run and mode == 'deep':
        click.echo("\n【提示】深度模式的实际页面修改请使用:")
        click.echo("  wiki link --source <页面> --target <页面> --strategy <策略>")


@cli.command()
@click.option('--force', is_flag=True, help='强制重建全部索引')
@click.option('--provider', type=str, help='临时指定 embedding 提供者')
@click.pass_context
def index(ctx, force: bool, provider: Optional[str]):
    """
    建立或更新 wiki 的 embedding 索引

    示例：
        wiki index
        wiki index --force
        wiki index --provider ollama
    """
    LOG.info("index: force=%s provider=%s", force, provider)
    wiki = ctx.obj['wiki']
    root = ctx.obj['root']

    config = load_config(root)
    embedding_cfg = config.get('embedding', {})

    if not embedding_cfg.get('enabled', False):
        click.echo("错误：embedding 未启用。请在 config.yaml 中设置 embedding.enabled: true")
        ctx.exit(1)

    if provider:
        embedding_cfg['provider'] = provider
        config['embedding'] = embedding_cfg

    try:
        provider_obj = create_provider(config)
    except Exception as e:
        click.echo(f"错误：初始化 embedding 提供者失败: {e}")
        ctx.exit(1)

    if provider_obj is None:
        click.echo("错误：无法创建 embedding 提供者。请检查 config.yaml 配置")
        ctx.exit(1)

    click.echo(f"使用提供者: {provider_obj.name}")
    click.echo("正在建立索引...")

    idx = EmbeddingIndex(wiki, provider_obj)
    indexed, skipped = idx.build(force=force)

    click.echo(f"\n[OK] 索引完成")
    click.echo(f"  新索引/更新: {indexed} 个页面")
    click.echo(f"  跳过（未变更）: {skipped} 个页面")


@cli.command()
@click.option('--fix', is_flag=True, help='尝试自动修复问题')
@click.pass_context
def lint(ctx, fix: bool):
    """
    检查 wiki 健康状况

    检查项：
      - 孤儿页面（未被引用的页面）
      - 死链（链接目标不是 wiki 目录下的文件 stem）
      - 陈旧页面（90天未更新）
      - 空页面（无有效正文）
      - 重复标题（多个文件声明同一页面）
      - 非 canonical 链接（链接目标未指向真实文件 stem）
      - 草稿页面
    """
    LOG.info("lint: fix=%s", fix)
    wiki = ctx.obj['wiki']

    click.echo("正在检查 wiki 健康状况...\n")

    issues = wiki.lint()

    has_issues = any(issues.values())

    if not has_issues:
        click.echo("[OK] 健康状况良好！")
        return

    # 报告问题
    if issues['orphans']:
        click.echo(f"[!] 孤儿页面 ({len(issues['orphans'])}):")
        for p in issues['orphans'][:5]:
            click.echo(f"    - {p}")
        if len(issues['orphans']) > 5:
            click.echo(f"    ... 还有 {len(issues['orphans']) - 5} 个")

    if issues['dead_links']:
        click.echo(f"\n[!] 死链 ({len(issues['dead_links'])}):")
        for link in issues['dead_links'][:5]:
            click.echo(f"    - [[{link}]]")

    if issues['stale']:
        click.echo(f"\n[OLD] 陈旧页面 ({len(issues['stale'])}):")
        for p in issues['stale'][:5]:
            click.echo(f"    - {p}")

    if issues['empty_pages']:
        click.echo(f"\n[EMPTY] 空页面 ({len(issues['empty_pages'])}):")
        for p in issues['empty_pages'][:5]:
            click.echo(f"    - {p}")

    if issues['duplicate_titles']:
        click.echo(f"\n[DUP] 重复标题 ({len(issues['duplicate_titles'])}):")
        for p in issues['duplicate_titles'][:5]:
            click.echo(f"    - {p}")

    if issues['noncanonical_links']:
        click.echo(f"\n[LINK] 非 canonical 链接 ({len(issues['noncanonical_links'])}):")
        for p in issues['noncanonical_links'][:5]:
            click.echo(f"    - {p}")

    if issues['drafts']:
        click.echo(f"\n[DRAFT] 草稿页面 ({len(issues['drafts'])}):")
        for p in issues['drafts'][:5]:
            click.echo(f"    - {p}")

    click.echo(f"\n请使用自然语言指令修复：")
    click.echo(f'  "请修复 wiki 中的问题"')


@cli.command()
@click.pass_context
def status(ctx):
    """查看 wiki 状态概览"""
    LOG.info("status")
    wiki = ctx.obj['wiki']
    root = ctx.obj['root']

    pages = wiki.list_pages()
    recent_logs = wiki.read_log(5)

    click.echo(f"[Wiki] 根目录: {root}")
    click.echo(f"[Pages] 总页面数: {len(pages)}")

    # 状态统计
    status_count = {}
    for p in pages:
        s = p.status
        status_count[s] = status_count.get(s, 0) + 1

    click.echo(f"\n页面状态:")
    for status, count in status_count.items():
        click.echo(f"  - {status}: {count}")

    click.echo(f"\n最近活动:")
    for entry in recent_logs:
        # 简化显示
        lines = entry.strip().split('\n')
        if lines:
            click.echo(f"  {lines[0]}")


if __name__ == '__main__':
    cli()
