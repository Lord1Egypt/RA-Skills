def get_recommended_config(service_type):
    # Common cache rule for files that shouldn't be cached
    no_cache_rule = {
        "CacheAction": {
            "Action": "cache",
            "IgnoreCase": False,
            "Ttl": 0,
            "DefaultPolicy": "no_cache"
        },
        "Condition": {
            "ConditionRule": [
                {
                    "Object": "filetype",
                    "Operator": "match",
                    "Type": "url",
                    "Value": "php;jsp;asp;aspx"
                }
            ]
        }
    }
    
    # Mandatory default cache rule for all unmatched requests
    default_cache_rule = {
        "CacheAction": {
            "Action": "cache",
            "IgnoreCase": False,
            "Ttl": 2592000,
            "DefaultPolicy": "default"
        },
        "Condition": {
            "ConditionRule": [
                {
                    "Object": "path",
                    "Operator": "match",
                    "Type": "url",
                    "Value": "/*"
                }
            ]
        }
    }
    
    base_config = {
        "Cache": [no_cache_rule, default_cache_rule]
    }
    
    if service_type == 'web':
        return {
            **base_config,
            "CacheKey": [
                {
                    "CacheKeyAction": {
                        "CacheKeyComponents": [
                            {
                                "Action": "include",
                                "IgnoreCase": False,
                                "Object": "queryString",
                                "Subobject": "*"
                            }
                        ]
                    },
                    "Condition": {
                        "ConditionRule": [
                            {
                                "Object": "directory",
                                "Operator": "match",
                                "Type": "url",
                                "Value": "/"
                            }
                        ]
                    }
                }
            ],
            "Compression": {
                "Switch": True,
                "CompressionRules": [
                    {
                        "CompressionAction": {
                            "CompressionFormat": "default",
                            "CompressionTarget": "*",
                            "CompressionType": ["gzip"]
                        }
                    }
                ]
            },
            "PageOptimization": {
                "PageOptimizationAction": "on"
            }
        }
        
    elif service_type == 'download':
        return {
            **base_config,
            "CacheKey": [
                {
                    "CacheKeyAction": {
                        "CacheKeyComponents": [
                            {
                                "Action": "exclude",
                                "IgnoreCase": False,
                                "Object": "queryString",
                                "Subobject": "*"
                            }
                        ]
                    },
                    "Condition": {
                        "ConditionRule": [
                            {
                                "Object": "directory",
                                "Operator": "match",
                                "Type": "url",
                                "Value": "/"
                            }
                        ]
                    }
                }
            ],
            "OriginRange": True,
            "FollowRedirect": True,
            "MultiRange": {
                "Switch": True
            }
        }
        
    elif service_type == 'video':
        return {
            **base_config,
            "CacheKey": [
                {
                    "CacheKeyAction": {
                        "CacheKeyComponents": [
                            {
                                "Action": "exclude",
                                "IgnoreCase": False,
                                "Object": "queryString",
                                "Subobject": "*"
                            }
                        ]
                    },
                    "Condition": {
                        "ConditionRule": [
                            {
                                "Object": "directory",
                                "Operator": "match",
                                "Type": "url",
                                "Value": "/"
                            }
                        ]
                    }
                }
            ],
            "OriginRange": True,
            "FollowRedirect": True,
            "MultiRange": {
                "Switch": True
            },
            "VideoDrag": {
                "Switch": True
            }
        }
    
    return {}
