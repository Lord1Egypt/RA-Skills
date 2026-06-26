"""
Basic usage examples for env-config-manager
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from env_manager import load_env, save_env, switch_env, get_var, set_var, validate_schema, diff_env


def example_load_and_read():
    """Load a .env file and read values."""
    # Create a sample .env file
    sample = {
        "APP_NAME": "MyApp",
        "DEBUG": "true",
        "PORT": "8080"
    }
    save_env(sample, ".env.sample")
    
    # Load it back
    env = load_env(".env.sample")
    print("Loaded environment:")
    for k, v in env.items():
        print(f"  {k} = {v}")
    
    os.remove(".env.sample")


def example_validate():
    """Validate environment against a schema."""
    env = {
        "DATABASE_URL": "postgresql://localhost/mydb",
        "PORT": "5432",
        "DEBUG": "false"
    }
    schema = {
        "DATABASE_URL": {"required": True, "type": "url"},
        "PORT": {"required": True, "type": "int", "min": 1024, "max": 65535},
        "DEBUG": {"required": False, "type": "bool", "default": False}
    }
    errors = validate_schema(env, schema)
    if errors:
        print("Validation errors:")
        for e in errors:
            print(f"  - {e}")
    else:
        print("Validation passed!")


def example_diff():
    """Compare two environment configurations."""
    env_dev = {"API_URL": "http://localhost:3000", "DEBUG": "true"}
    env_prod = {"API_URL": "https://api.example.com", "DEBUG": "false", "CACHE_TTL": "3600"}
    
    diff = diff_env(env_dev, env_prod)
    print("Differences between dev and prod:")
    for key, change in diff.items():
        print(f"  {key}: {change['old']} -> {change['new']}")


def example_switch():
    """Switch between environment files."""
    # Create dev and prod env files
    save_env({"API_URL": "http://localhost:3000", "DEBUG": "true"}, ".env.development")
    save_env({"API_URL": "https://api.example.com", "DEBUG": "false"}, ".env.production")
    
    # Switch to production
    env = switch_env("production")
    print("Switched to production:")
    print(f"  API_URL = {env.get('API_URL')}")
    
    # Cleanup
    os.remove(".env.development")
    os.remove(".env.production")


if __name__ == "__main__":
    print("=" * 50)
    print("Example 1: Load and Read")
    print("=" * 50)
    example_load_and_read()
    
    print("\n" + "=" * 50)
    print("Example 2: Validate")
    print("=" * 50)
    example_validate()
    
    print("\n" + "=" * 50)
    print("Example 3: Diff")
    print("=" * 50)
    example_diff()
    
    print("\n" + "=" * 50)
    print("Example 4: Switch")
    print("=" * 50)
    example_switch()
