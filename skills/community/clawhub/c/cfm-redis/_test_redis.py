import redis
print("redis version:", redis.__version__)
r = redis.Redis(host='localhost', port=6379)
r.ping()
print("Redis connected OK")
