#!/usr/bin/env python3
"""
AccessMind Interactive Report Generator
Detaylı ve görsel erişilebilirlik raporları oluşturur.
"""

import json
import base64
from datetime import datetime
from typing import Dict, List, Any

class AccessibilityReport:
    """Erişilebilirlik raporu oluşturucu"""
    
    def __init__(self, audit_data: Dict):
        self.data = audit_data
        self.generated_at = datetime.now().strftime("%d %B %Y, %H:%M")
    
    def generate_html_report(self, output_path: str):
        """Interaktif HTML rapor oluştur"""
        html = self._build_html()
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        return output_path
    
    def _build_html(self) -> str:
        """HTML rapor yapısını oluştur"""
        return f'''<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WCAG 2.2 Erişilebilirlik Raporu - {self.data.get('site', 'Site')}</title>
    <style>
        {self._get_css()}
    </style>
</head>
<body>
    {self._build_header()}
    {self._build_summary()}
    {self._build_score_card()}
    {self._build_violations_table()}
    {self._build_page_breakdown()}
    {self._build_recommendations()}
    {self._build_code_fixes()}
    {self._build_footer()}
    
    <script>
        {self._get_javascript()}
    </script>
</body>
</html>'''
    
    def _get_css(self) -> str:
        """CSS stilleri"""
        return '''
        :root {
            --primary: #2563eb;
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
            --info: #3b82f6;
            --dark: #1f2937;
            --light: #f3f4f6;
        }
        
        * { box-sizing: border-box; margin: 0; padding: 0; }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f8fafc;
            color: #1f2937;
            line-height: 1.6;
        }
        
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        
        /* Header */
        .header {
            background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
            color: white;
            padding: 40px;
            border-radius: 12px;
            margin-bottom: 30px;
        }
        .header h1 { font-size: 28px; margin-bottom: 10px; }
        .header p { opacity: 0.9; font-size: 14px; }
        
        /* Stats Grid */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: white;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            text-align: center;
        }
        .stat-number {
            font-size: 36px;
            font-weight: 700;
            margin-bottom: 5px;
        }
        .stat-label {
            color: #6b7280;
            font-size: 13px;
        }
        .stat-card.critical .stat-number { color: var(--danger); }
        .stat-card.serious .stat-number { color: var(--warning); }
        .stat-card.moderate .stat-number { color: #8b5cf6; }
        
        /* Score Card */
        .score-card {
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }
        .score-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }
        .score-value {
            font-size: 48px;
            font-weight: 700;
        }
        .score-good { color: var(--success); }
        .score-moderate { color: var(--warning); }
        .score-poor { color: var(--danger); }
        
        /* Progress Bar */
        .progress-bar {
            height: 20px;
            background: #e5e7eb;
            border-radius: 10px;
            overflow: hidden;
            margin: 15px 0;
        }
        .progress-fill {
            height: 100%;
            border-radius: 10px;
            transition: width 1s ease-out;
        }
        .progress-fill.good { background: var(--success); }
        .progress-fill.moderate { background: var(--warning); }
        .progress-fill.poor { background: var(--danger); }
        
        /* Violations Table */
        .violations-section {
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }
        .section-title {
            font-size: 20px;
            font-weight: 600;
            margin-bottom: 20px;
            color: #1f2937;
        }
        .violations-table {
            width: 100%;
            border-collapse: collapse;
        }
        .violations-table th {
            background: #f8fafc;
            padding: 15px;
            text-align: left;
            font-weight: 600;
            border-bottom: 2px solid #e5e7eb;
        }
        .violations-table td {
            padding: 15px;
            border-bottom: 1px solid #e5e7eb;
        }
        .violations-table tr:hover {
            background: #f8fafc;
        }
        .badge {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
        }
        .badge-critical { background: #fef2f2; color: #dc2626; }
        .badge-serious { background: #fffbeb; color: #d97706; }
        .badge-moderate { background: #f3e8ff; color: #7c3aed; }
        .badge-a { background: #fef2f2; color: #dc2626; }
        .badge-aa { background: #fffbeb; color: #d97706; }
        
        /* Page Breakdown */
        .page-card {
            background: white;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid var(--danger);
            margin-bottom: 15px;
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        }
        .page-card.good { border-left-color: var(--success); }
        .page-card.moderate { border-left-color: var(--warning); }
        .page-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }
        .page-title { font-weight: 600; color: #1f2937; }
        .page-url { font-size: 12px; color: #6b7280; }
        .page-stats {
            display: flex;
            gap: 20px;
            font-size: 13px;
            color: #4b5563;
        }
        
        /* Code Block */
        .code-block {
            background: #1f2937;
            color: #e5e7eb;
            padding: 20px;
            border-radius: 8px;
            font-family: 'Monaco', 'Consolas', monospace;
            font-size: 13px;
            overflow-x: auto;
            margin: 15px 0;
        }
        .code-block .comment { color: #6b7280; }
        .code-block .tag { color: #f472b6; }
        .code-block .attr { color: #a78bfa; }
        .code-block .value { color: #34d399; }
        
        /* Recommendations */
        .recommendation-card {
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 15px;
            border: 1px solid #e5e7eb;
        }
        .recommendation-header {
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 15px;
        }
        .recommendation-icon {
            width: 40px;
            height: 40px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
        }
        .recommendation-title { font-weight: 600; }
        .recommendation-meta { font-size: 12px; color: #6b7280; }
        .recommendation-steps {
            list-style: none;
            padding-left: 20px;
        }
        .recommendation-steps li {
            padding: 8px 0;
            border-bottom: 1px solid #f3f4f6;
        }
        .recommendation-steps li:last-child { border-bottom: none; }
        
        /* Tabs */
        .tabs {
            display: flex;
            border-bottom: 2px solid #e5e7eb;
            margin-bottom: 20px;
        }
        .tab {
            padding: 12px 24px;
            cursor: pointer;
            border-bottom: 2px solid transparent;
            margin-bottom: -2px;
            color: #6b7280;
            font-weight: 500;
        }
        .tab.active {
            border-bottom-color: var(--primary);
            color: var(--primary);
        }
        .tab-content { display: none; }
        .tab-content.active { display: block; }
        
        /* Footer */
        .footer {
            text-align: center;
            padding: 30px;
            color: #6b7280;
            font-size: 13px;
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            .stats-grid { grid-template-columns: repeat(2, 1fr); }
            .score-header { flex-direction: column; }
            .violations-table { font-size: 12px; }
        }
        
        /* Print */
        @media print {
            body { background: white; }
            .header { background: #1f2937; }
            .stat-card, .score-card, .violations-section { box-shadow: none; border: 1px solid #e5e7eb; }
        }
        '''
    
    def _build_header(self) -> str:
        """Rapor başlığı"""
        return f'''
        <div class="container">
            <div class="header">
                <h1>🔍 WCAG 2.2 Erişilebilirlik Raporu</h1>
                <p>{self.data.get('site', 'Site')} • {self.generated_at}</p>
                <p>Taranan sayfa: {self.data.get('pages_scanned', 0)} • AccessMind Denetim Sistemi</p>
            </div>
        '''
    
    def _build_summary(self) -> str:
        """Özet istatistikler"""
        score = self.data.get('score', 0)
        critical = self.data.get('critical_violations', 0)
        serious = self.data.get('serious_violations', 0)
        moderate = self.data.get('moderate_violations', 0)
        
        return f'''
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number">{self.data.get('pages_scanned', 0)}</div>
                    <div class="stat-label">Taranan Sayfa</div>
                </div>
                <div class="stat-card critical">
                    <div class="stat-number">{critical}</div>
                    <div class="stat-label">🔴 Kritik İhlal</div>
                </div>
                <div class="stat-card serious">
                    <div class="stat-number">{serious}</div>
                    <div class="stat-label">🟠 Ciddi İhlal</div>
                </div>
                <div class="stat-card moderate">
                    <div class="stat-number">{moderate}</div>
                    <div class="stat-label">🟡 Orta İhlal</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{self.data.get('wcag_aa_compliance', 0)}%</div>
                    <div class="stat-label">WCAG AA Uyumluluk</div>
                </div>
            </div>
        '''
    
    def _build_score_card(self) -> str:
        """Skor kartı"""
        score = self.data.get('score', 0)
        score_class = 'good' if score >= 80 else 'moderate' if score >= 60 else 'poor'
        progress_class = 'good' if score >= 80 else 'moderate' if score >= 60 else 'poor'
        
        return f'''
            <div class="score-card">
                <div class="score-header">
                    <div>
                        <div class="section-title">Erişilebilirlik Skoru (QAS)</div>
                        <p style="color: #6b7280; font-size: 14px;">Quantitative Accessibility Score</p>
                    </div>
                    <div class="score-value score-{score_class}">{score}/100</div>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill {progress_class}" style="width: {score}%"></div>
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 12px; color: #6b7280;">
                    <span>0 - Kritik</span>
                    <span>60 - Orta</span>
                    <span>80 - İyi</span>
                    <span>100 - Mükemmel</span>
                </div>
            </div>
        '''
    
    def _build_violations_table(self) -> str:
        """İhlal tablosu"""
        violations = self.data.get('violations', [])
        
        rows = ''
        for v in violations[:20]:  # İlk 20 ihlal
            severity_class = 'critical' if v.get('severity') == 'critical' else 'serious' if v.get('severity') == 'serious' else 'moderate'
            level_class = 'a' if v.get('level') == 'A' else 'aa'
            rows += f'''
                <tr>
                    <td><span class="badge badge-{severity_class}">{v.get('severity', 'moderate').upper()}</span></td>
                    <td><span class="badge badge-{level_class}">{v.get('level', 'A')}</span></td>
                    <td><strong>{v.get('rule', 'WCAG')}</strong></td>
                    <td>{v.get('description', '')}</td>
                    <td>{v.get('count', 1)}</td>
                    <td>{v.get('pages', '-')}</td>
                </tr>
            '''
        
        return f'''
            <div class="violations-section">
                <h2 class="section-title">📋 İhlal Listesi</h2>
                <div class="tabs">
                    <div class="tab active" onclick="showTab('all')">Tümü</div>
                    <div class="tab" onclick="showTab('critical')">Kritik</div>
                    <div class="tab" onclick="showTab('serious')">Ciddi</div>
                    <div class="tab" onclick="showTab('moderate')">Orta</div>
                </div>
                <table class="violations-table">
                    <thead>
                        <tr>
                            <th>Öncelik</th>
                            <th>Seviye</th>
                            <th>WCAG Kuralı</th>
                            <th>Açıklama</th>
                            <th>Sayı</th>
                            <th>Sayfalar</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows}
                    </tbody>
                </table>
            </div>
        '''
    
    def _build_page_breakdown(self) -> str:
        """Sayfa bazlı sonuçlar"""
        pages = self.data.get('pages', [])
        
        cards = ''
        for page in pages:
            score = page.get('score', 0)
            card_class = 'good' if score >= 80 else 'moderate' if score >= 60 else ''
            cards += f'''
                <div class="page-card {card_class}">
                    <div class="page-header">
                        <div>
                            <div class="page-title">{page.get('name', 'Sayfa')}</div>
                            <div class="page-url">{page.get('url', '')}</div>
                        </div>
                        <div class="stat-number" style="font-size: 24px;">{score}</div>
                    </div>
                    <div class="page-stats">
                        <span>📊 {page.get('size', 0)} KB</span>
                        <span>🖼️ {page.get('images', 0)} görsel</span>
                        <span>🔗 {page.get('links', 0)} link</span>
                        <span>❌ {page.get('violations', 0)} ihlal</span>
                    </div>
                </div>
            '''
        
        return f'''
            <div class="violations-section">
                <h2 class="section-title">📄 Sayfa Bazlı Sonuçlar</h2>
                {cards}
            </div>
        '''
    
    def _build_recommendations(self) -> str:
        """Düzeltme önerileri"""
        recommendations = [
            {
                'icon': '🖼️',
                'title': 'Görsellere Alt Metin Ekle',
                'priority': 'Kritik',
                'effort': '2-4 saat',
                'impact': 'Yüksek',
                'steps': [
                    'Tüm ürün görsellerine açıklayıcı alt metin ekleyin',
                    'Dekoratif görseller için alt="" kullanın',
                    'Karmaşık görseller için long description sağlayın',
                ]
            },
            {
                'icon': '📝',
                'title': 'Başlık Hiyerarşisini Düzelt',
                'priority': 'Kritik',
                'effort': '1-2 saat',
                'impact': 'Yüksek',
                'steps': [
                    'Her sayfada tek H1 başlığı kullanın',
                    'H1 → H2 → H3 sıralı geçiş yapın',
                    'Başlıkları anlamlı ve açıklayıcı yapın',
                ]
            },
            {
                'icon': '🔗',
                'title': 'Link Metinlerini İyileştir',
                'priority': 'Ciddi',
                'effort': '2-3 saat',
                'impact': 'Orta',
                'steps': [
                    'Boş linklere aria-label ekleyin',
                    '"Buraya tıklayın" yerine açıklayıcı metin kullanın',
                    'Link amacını metinden anlaşılır yapın',
                ]
            },
            {
                'icon': '⌨️',
                'title': 'Klavye Erişilebilirliğini Sağla',
                'priority': 'Ciddi',
                'effort': '4-6 saat',
                'impact': 'Yüksek',
                'steps': [
                    'Skip link ekleyin',
                    'Focus stillerini görünür yapın',
                    'Modal ve dropdown için focus trap uygulayın',
                ]
            },
        ]
        
        cards = ''
        for r in recommendations:
            cards += f'''
                <div class="recommendation-card">
                    <div class="recommendation-header">
                        <div class="recommendation-icon" style="background: #f3f4f6;">{r['icon']}</div>
                        <div>
                            <div class="recommendation-title">{r['title']}</div>
                            <div class="recommendation-meta">Öncelik: {r['priority']} • Efor: {r['effort']} • Etki: {r['impact']}</div>
                        </div>
                    </div>
                    <ol class="recommendation-steps">
                        {''.join(f'<li>{step}</li>' for step in r['steps'])}
                    </ol>
                </div>
            '''
        
        return f'''
            <div class="violations-section">
                <h2 class="section-title">🔧 Düzeltme Önerileri</h2>
                {cards}
            </div>
        '''
    
    def _build_code_fixes(self) -> str:
        """Kod düzeltmeleri"""
        return f'''
            <div class="violations-section">
                <h2 class="section-title">💻 Kod Düzeltmeleri</h2>
                
                <h3 style="margin: 20px 0 10px;">1. Görsel Alt Metni (WCAG 1.1.1)</h3>
                <div class="code-block">
<span class="comment">// Önce:</span>
<span class="tag">&lt;img</span> <span class="attr">src</span>=<span class="value">"product.jpg"</span> <span class="attr">class</span>=<span class="value">"product-image"</span><span class="tag">&gt;</span>

<span class="comment">// Sonra:</span>
<span class="tag">&lt;img</span> <span class="attr">src</span>=<span class="value">"product.jpg"</span> 
     <span class="attr">alt</span>=<span class="value">"Arçelik No-Frost Buzdolabı, 450 litre"</span>
     <span class="attr">class</span>=<span class="value">"product-image"</span><span class="tag">&gt;</span>
                </div>
                
                <h3 style="margin: 20px 0 10px;">2. Skip Link (WCAG 2.4.1)</h3>
                <div class="code-block">
<span class="comment">&lt;!-- HTML --&gt;</span>
<span class="tag">&lt;a</span> <span class="attr">href</span>=<span class="value">"#main-content"</span> <span class="attr">class</span>=<span class="value">"skip-link"</span><span class="tag">&gt;</span>
    İçeriğe atla
<span class="tag">&lt;/a&gt;</span>

<span class="comment">&lt;!-- CSS --&gt;</span>
<span class="tag">.skip-link</span> {{
    <span class="attr">position</span>: <span class="value">absolute</span>;
    <span class="attr">top</span>: <span class="value">-40px</span>;
    <span class="attr">left</span>: <span class="value">0</span>;
    <span class="attr">background</span>: <span class="value">#000</span>;
    <span class="attr">color</span>: <span class="value">#fff</span>;
    <span class="attr">padding</span>: <span class="value">8px</span>;
    <span class="attr">z-index</span>: <span class="value">100</span>;
}}
<span class="tag">.skip-link:focus</span> {{
    <span class="attr">top</span>: <span class="value">0</span>;
}}
                </div>
                
                <h3 style="margin: 20px 0 10px;">3. Form Etiketleri (WCAG 3.3.2)</h3>
                <div class="code-block">
<span class="comment">// Önce:</span>
<span class="tag">&lt;input</span> <span class="attr">type</span>=<span class="value">"email"</span> <span class="attr">placeholder</span>=<span class="value">"E-posta"</span><span class="tag">&gt;</span>

<span class="comment">// Sonra:</span>
<span class="tag">&lt;label</span> <span class="attr">for</span>=<span class="value">"email"</span><span class="tag">&gt;</span>E-posta<span class="tag">&lt;/label&gt;</span>
<span class="tag">&lt;input</span> <span class="attr">type</span>=<span class="value">"email"</span> 
       <span class="attr">id</span>=<span class="value">"email"</span>
       <span class="attr">name</span>=<span class="value">"email"</span>
       <span class="attr">aria-required</span>=<span class="value">"true"</span>
       <span class="attr">autocomplete</span>=<span class="value">"email"</span><span class="tag">&gt;</span>
                </div>
            </div>
        '''
    
    def _build_footer(self) -> str:
        """Rapor altbilgisi"""
        return f'''
            <div class="footer">
                <p>🔍 AccessMind WCAG 2.2 Denetim Sistemi</p>
                <p>Rapor Tarihi: {self.generated_at}</p>
                <p>Cloudflare bypass ile {self.data.get('pages_scanned', 0)} sayfa tarandı</p>
            </div>
        </div>
        '''
    
    def _get_javascript(self) -> str:
        """JavaScript kodu"""
        return '''
        // Tab switching
        function showTab(tabName) {
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            event.target.classList.add('active');
            document.getElementById(tabName).classList.add('active');
        }
        
        // Animate progress bar on load
        document.addEventListener('DOMContentLoaded', function() {
            const progressBars = document.querySelectorAll('.progress-fill');
            progressBars.forEach(bar => {
                const width = bar.style.width;
                bar.style.width = '0';
                setTimeout(() => {
                    bar.style.width = width;
                }, 100);
            });
        });
        '''


def main():
    """Test verisi ile örnek rapor oluştur"""
    test_data = {
        'site': 'arcelik.com.tr',
        'pages_scanned': 14,
        'score': 62,
        'critical_violations': 8,
        'serious_violations': 15,
        'moderate_violations': 23,
        'wcag_aa_compliance': 45,
        'violations': [
            {'severity': 'critical', 'level': 'A', 'rule': 'WCAG 1.1.1', 'description': 'Görsel alt metni eksik', 'count': 23, 'pages': '14 sayfa'},
            {'severity': 'critical', 'level': 'A', 'rule': 'WCAG 1.3.1', 'description': 'H1 başlığı eksik veya çoklu', 'count': 8, 'pages': '8 sayfa'},
            {'severity': 'serious', 'level': 'A', 'rule': 'WCAG 2.4.4', 'description': 'Boş link metinleri', 'count': 15, 'pages': '13 sayfa'},
            {'severity': 'serious', 'level': 'A', 'rule': 'WCAG 2.4.1', 'description': 'Skip link eksik', 'count': 14, 'pages': '14 sayfa'},
            {'severity': 'moderate', 'level': 'AA', 'rule': 'WCAG 2.4.7', 'description': 'Focus stili yetersiz', 'count': 10, 'pages': '10 sayfa'},
        ],
        'pages': [
            {'name': 'Ana Sayfa', 'url': 'https://arcelik.com.tr', 'score': 58, 'size': 485, 'images': 195, 'links': 120, 'violations': 5},
            {'name': 'Buzdolabı', 'url': 'https://arcelik.com.tr/buzdolabi', 'score': 65, 'size': 771, 'images': 257, 'links': 150, 'violations': 3},
            {'name': 'İletişim', 'url': 'https://arcelik.com.tr/iletisim', 'score': 42, 'size': 345, 'images': 107, 'links': 50, 'violations': 8},
        ]
    }
    
    report = AccessibilityReport(test_data)
    output_path = '/Users/sarper/.openclaw/workspace/test-report.html'
    report.generate_html_report(output_path)
    print(f"✅ Rapor oluşturuldu: {output_path}")


if __name__ == '__main__':
    main()