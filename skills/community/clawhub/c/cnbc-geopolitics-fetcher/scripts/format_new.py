# New format template - copy and paste the whole function below

def format_single_article(article):
    """Format a SINGLE article for Discord posting (one at a time) - NO TRUNCATION."""
    if not article.get('title'):
        return None
    
    # Title: use full title (Discord handles long titles)
    title = article['title']
    
    # Market: use complete market impact string
    market = article.get('market_impact', 'See article')
    
    # Facts: use complete sentences as-is (NO truncation)
    facts = article.get('hard_facts', ['No facts extracted'])[:5]
    facts_text = ''
    for f in facts:
        # No truncation - use complete sentence as extracted
        facts_text += f"  - {f}\n"
    
    # NEW FORMAT - remove ### Article, keep everything else
    entry = f"**{title}**\n\n**URL:** {article['url']}\n\n**Market Impact:** {market}\n\n**Hard Facts:**\n{facts_text.strip()}\n\n*(Raw data - no editorial analysis)*"
    
    return entry

