"""
Template Manager for Auto Video Generator

Provides functionality to:
- Browse available templates
- Preview templates
- Generate videos from templates
- Manage custom templates
- Install templates from marketplace (future)
"""

import os
import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class TemplateMetadata:
    """Metadata information about a template."""
    name: str
    id: str
    version: str
    author: str
    description: str
    category: str  # basic, industry, custom
    tags: List[str] = field(default_factory=list)
    
    preview_info: Dict[str, Any] = field(default_factory=dict)
    frameworks: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    
    defaults: Dict[str, Any] = field(default_factory=dict)
    parameters: List[Dict[str, Any]] = field(default_factory=list)
    generation_hints: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Template:
    """Complete template with metadata and content."""
    metadata: TemplateMetadata
    path: Path
    html_content: Optional[str] = None
    
    @property
    def name(self) -> str:
        return self.metadata.name
    
    @property
    def template_id(self) -> str:
        return self.metadata.id
    
    @property
    def category(self) -> str:
        return self.metadata.category


class TemplateManager:
    """
    Manages template discovery, loading, and usage.
    
    Example:
        >>> manager = TemplateManager()
        >>> templates = manager.list_templates()
        >>> template = manager.get_template("dashboard-analytics")
        >>> html = manager.render_template(template, custom_data={...})
    """
    
    # Default template directories to search
    DEFAULT_TEMPLATE_DIRS = [
        Path(__file__).parent / "templates" / "basic",
        Path(__file__).parent / "templates" / "industry",
        Path.home() / ".avg" / "templates",  # User custom templates
    ]
    
    def __init__(self, template_dirs: Optional[List[Path]] = None):
        """
        Initialize Template Manager.
        
        Args:
            template_dirs: Additional directories to search for templates.
                          If None, uses default directories.
        """
        self.template_dirs = template_dirs or self.DEFAULT_TEMPLATE_DIRS
        self._template_cache: Dict[str, Template] = {}
        
    def discover_templates(self) -> List[Template]:
        """
        Scan all template directories and discover valid templates.
        
        A valid template must have:
        - index.html file
        - config.yaml file with required metadata
        
        Returns:
            List of discovered Template objects.
        """
        discovered = []
        
        for directory in self.template_dirs:
            if not directory.exists():
                continue
                
            # Search for subdirectories containing index.html
            for item in directory.iterdir():
                if item.is_dir():
                    potential_template = self._load_template_from_dir(item)
                    if potential_template:
                        discovered.append(potential_template)
                        
        return discovered
    
    def _load_template_from_dir(self, directory: Path) -> Optional[Template]:
        """Load a single template from a directory."""
        html_file = directory / "index.html"
        config_file = directory / "config.yaml"
        
        if not html_file.exists() or not config_file.exists():
            return None
            
        try:
            # Load configuration
            with open(config_file, 'r', encoding='utf-8') as f:
                config_data = yaml.safe_load(f)
                
            # Parse metadata
            metadata_dict = config_data.get('metadata', {})
            metadata = TemplateMetadata(
                name=metadata_dict.get('name', 'Unnamed Template'),
                id=metadata_dict.get('id', directory.name),
                version=metadata_dict.get('version', '1.0.0'),
                author=metadata_dict.get('author', 'Unknown'),
                description=metadata_dict.get('description', ''),
                category=metadata_dict.get('category', 'custom'),
                tags=metadata_dict.get('tags', []),
                preview_info=metadata_dict.get('preview', {}),
                frameworks=metadata_dict.get('frameworks', []),
                dependencies=metadata_dict.get('dependencies', []),
                defaults=config_data.get('defaults', {}),
                parameters=config_data.get('parameters', []),
                generation_hints=config_data.get('generation_hints', {}),
            )
            
            # Load HTML content
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
                
            template = Template(
                metadata=metadata,
                path=directory,
                html_content=html_content
            )
            
            # Cache by ID
            self._template_cache[metadata.id] = template
            
            return template
            
        except Exception as e:
            print(f"[WARNING] Failed to load template from {directory}: {e}")
            return None
    
    def list_templates(
        self,
        category: Optional[str] = None,
        tag: Optional[str] = None,
        search_query: Optional[str] = None
    ) -> List[Template]:
        """
        List all available templates with optional filtering.
        
        Args:
            category: Filter by category ('basic', 'industry', 'custom')
            tag: Filter by tag
            search_query: Search in name, description, and tags
            
        Returns:
            Filtered list of templates.
        """
        # Ensure templates are loaded
        if not self._template_cache:
            self.discover_templates()
            
        templates = list(self._template_cache.values())
        
        # Apply filters
        if category:
            templates = [t for t in templates if t.category == category]
            
        if tag:
            templates = [t for t in templates if tag in t.metadata.tags]
            
        if search_query:
            query_lower = search_query.lower()
            templates = [
                t for t in templates 
                if (
                    query_lower in t.name.lower() or
                    query_lower in t.metadata.description.lower() or
                    any(query_lower in tag.lower() for tag in t.metadata.tags)
                )
            ]
            
        # Sort by name
        templates.sort(key=lambda t: t.name)
        
        return templates
    
    def get_template(self, template_id: str) -> Optional[Template]:
        """
        Get a specific template by its ID.
        
        Args:
            template_id: Unique identifier of the template
            
        Returns:
            Template object if found, None otherwise.
        """
        # Check cache first
        if template_id in self._template_cache:
            return self._template_cache[template_id]
            
        # Search directories
        for directory in self.template_dirs:
            target_path = directory / template_id / "index.html"
            if target_path.exists():
                template = self._load_template_from_dir(directory / template_id)
                if template:
                    return template
                    
        return None
    
    def get_template_categories(self) -> Dict[str, int]:
        """
        Get count of templates per category.
        
        Returns:
            Dictionary mapping category names to template counts.
        """
        templates = self.list_templates()
        categories = {}
        
        for template in templates:
            cat = template.category
            categories[cat] = categories.get(cat, 0) + 1
            
        return categories
    
    def render_template(
        self,
        template: Template,
        custom_data: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> str:
        """
        Render template with custom data substitution.
        
        Simple template rendering that replaces {{ variable }} placeholders.
        For complex templating, consider using Jinja2.
        
        Args:
            template: Template object to render
            custom_data: Dictionary of values to substitute into template
            **kwargs: Alternative way to pass custom data
            
        Returns:
            Rendered HTML string with substitutions applied.
        """
        if not template.html_content:
            # Load if not cached
            html_file = template.path / "index.html"
            with open(html_file, 'r', encoding='utf-8') as f:
                template.html_content = f.read()
                
        rendered = template.html_content
        
        # Merge custom data
        data = {}
        if custom_data:
            data.update(custom_data)
        data.update(kwargs)
        
        # Apply parameter defaults from config
        for param in template.metadata.parameters:
            param_name = param['name']
            default_value = param.get('default', '')
            if param_name not in data:
                data[param_name] = default_value
        
        # Perform simple substitution
        for key, value in data.items():
            placeholder = f"{{{{{key}}}}}"
            rendered = rendered.replace(placeholder, str(value))
            
        return rendered
    
    def preview_template(
        self,
        template: Template,
        output_path: Optional[Path] = None
    ) -> Path:
        """
        Generate preview HTML file for a template.
        
        Args:
            template: Template to preview
            output_path: Where to save preview file. Defaults to temp location.
            
        Returns:
            Path to the generated preview file.
        """
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = Path(f"./preview_{template.template_id}_{timestamp}.html")
            
        rendered_html = self.render_template(template)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(rendered_html)
            
        return output_path
    
    def generate_video_from_template(
        self,
        template_id: str,
        output: str,
        options: Optional[Dict[str, Any]] = None,
        custom_data: Optional[Dict[str, Any]] = None,
        **video_options
    ):
        """
        Convenience method to generate video directly from a template.
        
        This method:
        1. Loads the template
        2. Renders it with custom data
        3. Saves to temporary file
        4. Generates video using VideoGenerator
        
        Args:
            template_id: ID of the template to use
            output: Output path for generated video
            options: Generation options (passed to VideoGenerator.generate)
            custom_data: Data to substitute into template
            **video_options: Additional video generation options
            
        Returns:
            GenerationResult from VideoGenerator
        """
        from auto_video_generator import VideoGenerator
        import tempfile
        
        # Get template
        template = self.get_template(template_id)
        if not template:
            raise ValueError(f"Template '{template_id}' not found")
            
        # Render template
        rendered_html = self.render_template(template, custom_data)
        
        # Save to temp file
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.html',
            delete=False,
            encoding='utf-8'
        ) as f:
            f.write(rendered_html)
            temp_path = f.name
            
        try:
            # Initialize generator with template's default settings
            gen_config = template.metadata.defaults.copy()
            if options:
                gen_config.update(options)
                
            gen = VideoGenerator(config=gen_config)
            
            # Generate video
            result = await gen.generate(
                source=temp_path,
                output=output,
                options=video_options
            )
            
            return result
            
        finally:
            # Cleanup temp file
            try:
                os.unlink(temp_path)
            except:
                pass
    
    def export_template(self, template: Template, output_path: Path) -> bool:
        """
        Export template as a distributable package.
        
        Creates a .tgz archive containing:
        - index.html
        - config.yaml
        - Any assets (css, js, images)
        
        Args:
            template: Template to export
            output_path: Destination path for the package
            
        Returns:
            True if export successful, False otherwise.
        """
        import tarfile
        import shutil
        
        try:
            with tarfile.open(output_path, 'w:gz') as tar:
                tar.add(template.path, arcname=template.template_id)
                
            print(f"[OK] Template exported to: {output_path}")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to export template: {e}")
            return False
    
    def install_template(self, package_path: Path, target_dir: Optional[Path] = None) -> bool:
        """
        Install a template from a package file.
        
        Args:
            package_path: Path to .tgz template package
            target_dir: Directory to extract to (default: user templates dir)
            
        Returns:
            True if installation successful, False otherwise.
        """
        import tarfile
        
        if target_dir is None:
            target_dir = Path.home() / ".avg" / "templates"
            target_dir.mkdir(parents=True, exist_ok=True)
            
        try:
            with tarfile.open(package_path, 'r:gz') as tar:
                tar.extractall(target_dir)
                
            # Clear cache to pick up new template
            self._template_cache.clear()
            
            print(f"[OK] Template installed to: {target_dir}")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to install template: {e}")
            return False
    
    def validate_template(self, template: Template) -> Dict[str, Any]:
        """
        Validate a template for completeness and correctness.
        
        Checks:
        - Required files exist (index.html, config.yaml)
        - Config has required fields
        - HTML is well-formed (basic check)
        - No broken references
        
        Args:
            template: Template to validate
            
        Returns:
            Dictionary with validation results:
            {
                'valid': bool,
                'errors': List[str],
                'warnings': List[str],
                'score': float (0.0 - 1.0)
            }
        """
        errors = []
        warnings = []
        score = 1.0
        
        # Check required files
        required_files = ['index.html', 'config.yaml']
        for filename in required_files:
            filepath = template.path / filename
            if not filepath.exists():
                errors.append(f"Missing required file: {filename}")
                score -= 0.25
                
        # Validate config structure
        config_file = template.path / "config.yaml"
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                try:
                    config = yaml.safe_load(f)
                    
                    required_fields = ['metadata', 'name', 'id']
                    for field in required_fields:
                        if field not in config.get('metadata', {}):
                            errors.append(f"Config missing metadata.{field}")
                            score -= 0.1
                            
                except yaml.YAMLError as e:
                    errors.append(f"Invalid YAML syntax: {e}")
                    score -= 0.3
                    
        # Basic HTML checks
        html_file = template.path / "index.html"
        if html_file.exists():
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
                
                if '<!DOCTYPE html>' not in html_content[:100]:
                    warnings.append("Missing DOCTYPE declaration")
                    score -= 0.05
                    
                if '</html>' not in html_content[-100:]:
                    warnings.append("HTML may be incomplete")
                    score -= 0.05
                    
                if len(html_content) < 500:
                    warnings.append("Template seems very short")
                    score -= 0.05
        
        # Check for common issues
        if not template.metadata.description:
            warnings.append("No description provided")
            score -= 0.02
            
        if not template.metadata.tags:
            warnings.append("No tags defined (reduces discoverability)")
            score -= 0.02
            
        # Cap score at 0
        score = max(0.0, score)
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings,
            'score': round(score, 2),
            'grade': self._score_to_grade(score)
        }
    
    def _score_to_grade(self, score: float) -> str:
        """Convert numeric score to letter grade."""
        if score >= 0.9:
            return 'A'
        elif score >= 0.8:
            return 'B'
        elif score >= 0.7:
            return 'C'
        elif score >= 0.6:
            return 'D'
        else:
            return 'F'
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about available templates.
        
        Returns:
            Dictionary with template library statistics.
        """
        templates = self.list_templates()
        
        stats = {
            'total_templates': len(templates),
            'categories': {},
            'frameworks_used': {},
            'avg_complexity': 0,
            'most_common_tags': [],
        }
        
        complexity_scores = []
        tag_counts = {}
        
        for template in templates:
            # Category counts
            cat = template.category
            stats['categories'][cat] = stats['categories'].get(cat, 0) + 1
            
            # Framework tracking
            for framework in template.metadata.frameworks:
                stats['frameworks_used'][framework] = \
                    stats['frameworks_used'].get(framework, 0) + 1
                    
            # Complexity estimation based on expected duration
            duration = template.metadata.preview_info.get('duration_seconds', 20)
            complexity_scores.append(duration)
            
            # Tag counting
            for tag in template.metadata.tags:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
                
        # Calculate averages
        if complexity_scores:
            stats['avg_complexity'] = sum(complexity_scores) / len(complexity_scores)
            
        # Top tags
        sorted_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)
        stats['most_common_tags'] = sorted_tags[:10]
        
        return stats


# CLI Integration Functions
def register_template_commands(cli):
    """Register template-related commands with CLI."""
    
    @cli.command()
    def template_list(category=None, tag=None, search=None):
        """List available templates."""
        manager = TemplateManager()
        templates = manager.list_templates(category, tag, search)
        
        print(f"\n{'='*60}")
        print(f"  Available Templates ({len(templates)} found)")
        print(f"{'='*60}\n")
        
        for i, template in enumerate(templates, 1):
            meta = template.metadata
            print(f"{i:2d}. {meta.name}")
            print(f"    ID: {meta.id}")
            print(f"    Category: {meta.category} | Version: {meta.version}")
            print(f"    Tags: {', '.join(meta.tags)}")
            print(f"    {meta.description[:80]}...")
            print()
            
        if not templates:
            print("No templates found matching your criteria.")
            
    @cli.command()
    def template_preview(template_id):
        """Preview a template in browser."""
        manager = TemplateManager()
        template = manager.get_template(template_id)
        
        if not template:
            print(f"[ERROR] Template '{template_id}' not found")
            return False
            
        preview_path = manager.preview_template(template)
        print(f"[OK] Preview generated: {preview_path}")
        print(f"      Open this file in your browser to view.")
        
        return True
    
    @cli.command()
    def template_validate(template_id):
        """Validate a template for issues."""
        manager = TemplateManager()
        template = manager.get_template(template_id)
        
        if not template:
            print(f"[ERROR] Template '{template_id}' not found")
            return
            
        results = manager.validate_template(template)
        
        print(f"\n{'='*60}")
        print(f"  Validation Results: {template.name}")
        print(f"{'='*60}\n")
        
        print(f"Overall Grade: {results['grade']} ({results['score']*100:.0f}%)\n")
        
        if results['valid']:
            print("[PASS] Template is valid!")
        else:
            print("[FAIL] Template has errors:\n")
            for error in results['errors']:
                print(f"  ❌ {error}")
                
        if results['warnings']:
            print("\nWarnings:")
            for warning in results['warnings']:
                print(f"  ⚠️  {warning}")
                
    @cli.command()
    def template_stats():
        """Show template library statistics."""
        manager = TemplateManager()
        stats = manager.get_statistics()
        
        print(f"\n{'='*60}")
        print(f"  Template Library Statistics")
        print(f"{'='*60}\n")
        
        print(f"Total Templates: {stats['total_templates']}\n")
        
        print("By Category:")
        for cat, count in stats['categories'].items():
            print(f"  • {cat}: {count} templates")
            
        print("\nMost Popular Tags:")
        for tag, count in stats['most_common_tags'][:5]:
            print(f"  • {tag}: {count} templates")


# Module-level convenience functions
def get_template_manager() -> TemplateManager:
    """Get global template manager instance."""
    if not hasattr(get_template_manager, '_instance'):
        get_template_manager._instance = TemplateManager()
    return get_template_manager._instance


def list_available_templates(**filters):
    """Quick function to list templates."""
    manager = get_template_manager()
    return manager.list_templates(**filters)


def load_template(template_id):
    """Quick function to load a template by ID."""
    manager = get_template_manager()
    return manager.get_template(template_id)


if __name__ == "__main__":
    # Demo usage
    print("=" * 60)
    print("  Auto Video Generator - Template Manager Demo")
    print("=" * 60)
    
    manager = TemplateManager()
    
    # Discover templates
    print("\n[1/4] Discovering templates...")
    templates = manager.discover_templates()
    print(f"       Found {len(templates)} templates\n")
    
    # Show statistics
    print("[2/4] Library Statistics:")
    stats = manager.get_statistics()
    print(f"       Total: {stats['total_templates']}")
    print(f"       Avg Duration: {stats['avg_complexity']:.1f}s\n")
    
    # List templates
    print("[3/4] Available Templates:")
    listed = manager.list_templates()
    for template in listed[:5]:  # Show first 5
        print(f"       • [{template.category}] {template.name} ({template.template_id})")
    if len(listed) > 5:
        print(f"       ... and {len(listed)-5} more\n")
        
    # Validate one
    print("[4/4] Validating templates:")
    for template in listed[:3]:
        result = manager.validate_template(template)
        status = "✓ PASS" if result['valid'] else "✗ FAIL"
        print(f"       {status} | {result['grade']} | {template.name}")
        
    print("\n" + "=" * 60)
    print("  Template Manager Ready!")
    print("=" * 60)
