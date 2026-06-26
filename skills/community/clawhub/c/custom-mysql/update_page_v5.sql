-- Update WordPress page for VectorClaw v5.0.0
-- Run: docker exec -i myvector-db mysql -u root -p<pass> wordpress < update_page_v5.sql
-- (or update via wp-cli / REST API)

UPDATE wp_posts SET post_content = '<!-- wp:image {"align":"center","id":121,"sizeSlug":"large","linkDestination":"none"} -->
<figure class="wp-block-image aligncenter size-large"><img data-sf-processed="1" loading="lazy" decoding="async" width="1024" height="512" src="http://192.168.1.6/wp-content/uploads/2026/05/cf-img-1779267756872.jpg" alt="VectorClaw" class="wp-image-121" srcset="http://192.168.1.6/wp-content/uploads/2026/05/cf-img-1779267756872.jpg 1024w, http://192.168.1.6/wp-content/uploads/2026/05/cf-img-1779267756872-300x150.jpg 300w, http://192.168.1.6/wp-content/uploads/2026/05/cf-img-1779267756872-768x384.jpg 768w" sizes="auto, (max-width: 1024px) 100vw, 1024px" /></figure>
<!-- /wp:image -->

<!-- wp:paragraph -->
<p class="wp-block-paragraph"><strong>VectorClaw</strong> is a security-hardened MyVector MySQL skill for OpenClaw that gives your AI agent persistent, intelligent, self-sufficient memory. v5.0.0 makes <strong>MyVector the single source of truth</strong> — replacing external tools (Mem0, Hancho) with native auto-extraction and knowledge graph reasoning, all in MySQL.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">What''s New in v5.0.0</h2>
<!-- /wp:heading -->

<!-- wp:heading {"level":3} -->
<h3 class="wp-block-heading">Auto-Extraction Hook — Replaces Mem0</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>v5.0.0 adds a local LLM-powered extraction hook that <strong>automatically pulls atomic facts from conversation text</strong> and inserts them into MyVector. No external service needed:</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul class="wp-block-list"><li>Uses local qwen3.5:4b with structured JSON prompt</li><li>Extracts: core_fact, confidence, entities, linked_to, tags, memory_type, importance</li><li>Auto-dedup on insert: Jaccard similarity check, merges if &gt;50% overlap</li><li>Source tracking: auto-extracted memories marked with source=''auto''</li><li>Human verification flag for promoting accurate auto-facts</li><li>Quality logging to extraction_log for empirical tuning</li></ul>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":3} -->
<h3 class="wp-block-heading">Memory Relations + Knowledge Graph — Replaces Hancho</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Native MySQL knowledge graph with <strong>graph traversal during retrieval</strong>:</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul class="wp-block-list"><li>memory_relations table: fact_id, related_fact_id, relation_type, confidence</li><li>Relation types: mentions, implies, contradicts, same_entity, related_to</li><li>Auto-discovery during extraction: finds existing memories sharing entities</li><li>Consolidation pass: periodic scanning for contradictions and new edges</li><li>Hub insight derivation: identifies high-degree facts (3+ connections) as important</li><li>memory_graph_1hop view: pre-computed 1-hop traversal for fast retrieval</li></ul>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":3} -->
<h3 class="wp-block-heading">Source Tracking + Human Verification</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Every memory now tracks its provenance:</p>
<!-- /wp:paragraph -->

<!-- wp:table -->
<figure class="wp-block-table"><table><thead><tr><th>Source</th><th>Description</th><th>Initial Confidence</th></tr></thead><tbody><tr><td>manual</td><td>Written explicitly by agent</td><td>0.9</td></tr><tr><td>auto</td><td>Extracted by local LLM hook</td><td>0.6-0.7</td></tr><tr><td>consolidation</td><td>Derived from consolidation pass</td><td>0.7</td></tr><tr><td>import</td><td>Imported from external system</td><td>0.5</td></tr></tbody></table></figure>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Auto-extracted facts start at lower confidence and get promoted when verified by grounding checks during conversation.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">Memory Architecture (v5.0.0)</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>v5.0.0 completes the consolidation started in v4.0.0. The full memory stack:</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul class="wp-block-list"><li><strong>MEMORY.md</strong> — Always-in-context narrative (relationships, lessons, emotional context)</li><li><strong>MyVector (MySQL)</strong> — Structured profiles, facts, preferences, dimensional tags, knowledge graph edges, extraction logs</li><li><strong>ChromaDB</strong> — Semantic search across workspace files (skills, projects, logs)</li><li><strong>Retrieval Gate v3</strong> — Smart triggering: explicit signals, entity SQL pre-filter, depth mode, keyword Jaccard, embedding delta, graph expansion</li><li><strong>Grounding Protocol</strong> — Literal message quoting, delta detection, entity self-critique, memory source check</li><li><strong>Auto-Extraction</strong> — Local LLM extracts facts from every conversation turn</li><li><strong>Knowledge Graph</strong> — Native MySQL relations with contradiction detection</li></ul>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">Deprecation Plan</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>v5.0.0 is designed to make external memory tools unnecessary:</p>
<!-- /wp:paragraph -->

<!-- wp:table -->
<figure class="wp-block-table"><table><thead><tr><th>External Tool</th><th>Replacement</th><th>Migration</th></tr></thead><tbody><tr><td>Mem0</td><td>auto-extract.py (local LLM)</td><td>Run 7-10 days parallel, compare quality, then retire</td></tr><tr><td>Hancho</td><td>memory_relations + hancho-consolidate.py</td><td>Already native — retire after validation</td></tr></tbody></table></figure>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">How It Compares</h2>
<!-- /wp:heading -->

<!-- wp:table -->
<figure class="wp-block-table"><table><thead><tr><th>Feature</th><th>VectorClaw v5</th><th>Mem0</th><th>Supermemory</th></tr></thead><tbody><tr><td><strong>Storage</strong></td><td>Self-hosted MySQL (MyVector) — you own everything</td><td>Cloud-hosted</td><td>Cloud-hosted</td></tr><tr><td><strong>Auto-extraction</strong></td><td>✅ Local LLM (qwen3.5:4b) + regex fallback</td><td>✅ Managed NLP</td><td>✅ Managed NLP</td></tr><tr><td><strong>Dedup on insert</strong></td><td>✅ Jaccard similarity with merge</td><td>❌</td><td>❌</td></tr><tr><td><strong>Source tracking</strong></td><td>✅ manual/auto/consolidation/import</td><td>❌</td><td>❌</td></tr><tr><td><strong>Knowledge graph</td>strong></td><td>✅ Native MySQL edges + traversal view</td><td>❌</td><td>❌</td></tr><tr><td><strong>Contradiction detection</strong></td><td>✅ Polarity-based consolidation pass</td><td>❌</td><td>❌</td></tr><tr><td><strong>Post-conversation analysis</strong></td><td>✅ HindSight consolidation</td><td>❌</td><td>❌</td></tr><tr><td><strong>Multi-dimensional tags</strong></td><td>✅ HoloGraphic (emotion, context, urgency, people)</td><td>❌</td><td>❌</td></tr><tr><td><strong>Quality logging</strong></td><td>✅ extraction_log with per-run metrics</td><td>❌</td><td>❌</td></tr><tr><td><strong>Self-hosted</strong></td><td>✅ Full control, no API limits, no vendor lock-in</td><td>❌ Cloud dependency</td><td>❌ Cloud dependency</td></tr><tr><td><strong>Security</strong></td><td>✅ 20/20 audit score, least-privilege, DDL blocked</td><td>Basic</td><td>Basic</td></tr><tr><td><strong>Cost</strong></td><td>Free (self-hosted)</td><td>Free tier + paid</td><td>Free tier + paid</td></tr></tbody></table></figure>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">Requirements</h2>
<!-- /wp:heading -->

<!-- wp:list -->
<ul class="wp-block-list"><li>Docker (for MyVector container)</li><li>OpenClaw agent</li><li>Ollama with qwen3.5:4b (for auto-extraction)</li><li>~500MB RAM for the MyVector container</li></ul>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">Get It</h2>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>VectorClaw is available as a free OpenClaw skill on ClawHub:</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>🔗 <strong>ClawHub:</strong> <a href="https://clawhub.ai/paradoxfuzzle/custom-mysql">https://clawhub.ai/paradoxfuzzle/custom-mysql</a></p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Install with: <code>openclaw skills install custom-mysql</code></p>
<!-- /wp:paragraph -->

<!-- wp:paragraph {"align":"center"} -->
<p class="has-text-align-center wp-block-paragraph"><em>🐼 Remember everything. Reason about it. Grow from it. Own it all.</em></p>
<!-- /wp:paragraph -->' WHERE ID = 65;
